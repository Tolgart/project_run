from geopy.distance import distance
from .models import Position

def calculate_distance(run_id):
    total_distance_km = 0

    positions = Position.objects.filter(run=run_id)

    coords = [(p.latitude, p.longitude) for p in positions]

    if len(coords) < 2:
        return 0.0

    for i in range(len(coords) - 1):
        total_distance_km += distance(coords[i], coords[i + 1]).km

    return total_distance_km