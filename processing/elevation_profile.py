#!/usr/bin/env python3
"""Generate elevation profiles, gradient calculations, and power estimates per segment."""

import argparse
import json
import math
import os

import gpxpy
import numpy as np

# Reference rider parameters
RIDER_MASS = 70  # kg
BIKE_MASS = 8    # kg
TOTAL_MASS = RIDER_MASS + BIKE_MASS
CDA = 0.35       # drag area (m^2)
CRR = 0.005      # rolling resistance coefficient
RHO = 1.225      # air density (kg/m^3)
G = 9.81         # gravity (m/s^2)


def haversine(lat1, lon1, lat2, lon2):
    """Distance in meters between two points."""
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def calculate_power(gradient_pct, speed_kmh):
    """Calculate required power (watts) for given gradient and speed."""
    speed_ms = speed_kmh / 3.6
    grade = gradient_pct / 100.0

    # Rolling resistance
    p_roll = CRR * TOTAL_MASS * G * speed_ms

    # Gravity
    p_gravity = TOTAL_MASS * G * grade * speed_ms

    # Aerodynamic drag
    p_aero = 0.5 * RHO * CDA * speed_ms ** 3

    total = p_roll + p_gravity + p_aero
    return max(0, total)  # Can't have negative power (freewheeling)


def process_segment(gpx_path, segment_num):
    """Process a single segment GPX file into elevation profile data."""
    with open(gpx_path, "r") as f:
        gpx = gpxpy.parse(f)

    points = []
    cum_dist = 0.0

    for track in gpx.tracks:
        for segment in track.segments:
            for i, pt in enumerate(segment.points):
                if i > 0:
                    prev = segment.points[i - 1]
                    cum_dist += haversine(prev.latitude, prev.longitude, pt.latitude, pt.longitude)
                points.append({
                    "dist_m": cum_dist,
                    "ele": pt.elevation or 0,
                })

    if len(points) < 2:
        return None

    # Resample to ~50m intervals for smooth profiles
    total_dist = points[-1]["dist_m"]
    num_samples = max(int(total_dist / 50), 10)
    sample_dists = np.linspace(0, total_dist, num_samples)

    raw_dists = np.array([p["dist_m"] for p in points])
    raw_eles = np.array([p["ele"] for p in points])
    sampled_eles = np.interp(sample_dists, raw_dists, raw_eles)

    # Smooth elevation with a rolling average (~200m window) to dampen GPS-elevation noise.
    # 50m sample step × 4 samples = 200m. Earlier int(100/step) truncated 1.99→1, disabling
    # smoothing entirely and letting raw-GPX spikes (e.g. 12m drop in 50m → 24% gradient) show
    # up as max_*_gradient values. 200m is gentle enough to preserve real road features while
    # filtering single-point GPS anomalies.
    sample_step_m = total_dist / num_samples if num_samples else 50.0
    window = max(2, round(200 / sample_step_m))
    if window > 1 and len(sampled_eles) > window:
        kernel = np.ones(window) / window
        smoothed = np.convolve(sampled_eles, kernel, mode="same")
        # Keep endpoints from original
        smoothed[:window // 2] = sampled_eles[:window // 2]
        smoothed[-(window // 2):] = sampled_eles[-(window // 2):]
    else:
        smoothed = sampled_eles

    # Calculate gradients
    gradients = []
    for i in range(len(sample_dists)):
        if i == 0:
            gradients.append(0.0)
        else:
            dx = sample_dists[i] - sample_dists[i - 1]
            dy = smoothed[i] - smoothed[i - 1]
            gradients.append((dy / dx) * 100 if dx > 0 else 0.0)

    # Subsample for JSON output (~30 points per segment)
    output_count = min(30, len(sample_dists))
    indices = np.linspace(0, len(sample_dists) - 1, output_count, dtype=int)

    distance = [round(sample_dists[i] / 1000, 2) for i in indices]
    elevation = [round(float(smoothed[i]), 1) for i in indices]
    gradient = [round(float(gradients[i]), 1) for i in indices]

    # Power at four speeds
    power_30 = [round(calculate_power(g, 30)) for g in gradient]
    power_35 = [round(calculate_power(g, 35)) for g in gradient]
    power_40 = [round(calculate_power(g, 40)) for g in gradient]
    power_50 = [round(calculate_power(g, 50)) for g in gradient]

    # Summary stats
    all_gradients = np.array(gradients)
    ele_diffs = np.diff(smoothed)
    ele_gain = float(np.sum(ele_diffs[ele_diffs > 0]))
    ele_loss = float(np.sum(np.abs(ele_diffs[ele_diffs < 0])))

    total_km = total_dist / 1000

    climb_gradients = all_gradients[all_gradients > 0]
    descent_gradients = all_gradients[all_gradients < 0]

    summary = {
        "avg_gradient": round(float(np.mean(all_gradients[1:])), 1),
        "max_gradient": round(float(np.max(all_gradients)), 1),
        "avg_climb_gradient": round(float(np.mean(climb_gradients)), 1) if len(climb_gradients) > 0 else 0.0,
        "avg_descent_gradient": round(float(np.mean(descent_gradients)), 1) if len(descent_gradients) > 0 else 0.0,
        "max_climb_gradient": round(float(np.max(climb_gradients)), 1) if len(climb_gradients) > 0 else 0.0,
        "max_descent_gradient": round(float(np.min(descent_gradients)), 1) if len(descent_gradients) > 0 else 0.0,
        "elevation_gain": round(ele_gain),
        "elevation_loss": round(ele_loss),
        "avg_power_30kmh": round(float(np.mean(power_30))),
        "avg_power_35kmh": round(float(np.mean(power_35))),
        "avg_power_40kmh": round(float(np.mean(power_40))),
        "avg_power_50kmh": round(float(np.mean(power_50))),
        "estimated_time_30kmh": format_time(total_km / 30 * 60),
        "estimated_time_35kmh": format_time(total_km / 35 * 60),
        "estimated_time_40kmh": format_time(total_km / 40 * 60),
        "estimated_time_50kmh": format_time(total_km / 50 * 60),
        "time_unit": "hr:min" if total_km / 50 * 60 >= 60 else "min:sec",
    }

    return {
        "segment": segment_num,
        "distance": distance,
        "elevation": elevation,
        "gradient": gradient,
        "power_30kmh": power_30,
        "power_35kmh": power_35,
        "power_40kmh": power_40,
        "power_50kmh": power_50,
        "summary": summary,
    }


def format_time(minutes):
    """Format minutes as time string. Returns H:MM for >= 60min, M:SS otherwise."""
    if minutes >= 60:
        h = int(minutes // 60)
        m = int(minutes % 60)
        return f"{h}:{m:02d}"
    m = int(minutes)
    s = int((minutes - m) * 60)
    return f"{m}:{s:02d}"


def main():
    parser = argparse.ArgumentParser(description="Generate elevation profiles and power estimates")
    parser.add_argument("--segments-dir", default="data/segments", help="Directory with segment GPX files")
    parser.add_argument("--output-dir", default="data/elevation", help="Output directory for elevation JSON files")
    parser.add_argument("--num-segments", type=int, default=27)
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    for seg_num in range(1, args.num_segments + 1):
        seg_str = str(seg_num).zfill(2)
        gpx_path = os.path.join(args.segments_dir, f"segment-{seg_str}.gpx")

        if not os.path.exists(gpx_path):
            print(f"  Segment {seg_num}: GPX not found, skipping")
            continue

        result = process_segment(gpx_path, seg_num)
        if result is None:
            print(f"  Segment {seg_num}: insufficient data, skipping")
            continue

        output_path = os.path.join(args.output_dir, f"segment-{seg_str}.json")
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)

        s = result["summary"]
        print(f"  Segment {seg_num}: +{s['elevation_gain']}m/-{s['elevation_loss']}m, "
              f"avg grade {s['avg_gradient']}%, "
              f"avg power @35km/h: {s['avg_power_35kmh']}W")

    print(f"\nWrote elevation profiles to {args.output_dir}/")


if __name__ == "__main__":
    main()
