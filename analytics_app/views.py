from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from irctc.mongodb import api_logs

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def top_routes(request):
    pipeline = [
        {
            "$group": {
                "_id": {
                    "source": "$source",
                    "destination": "$destination"
                },
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"count": -1}
        },
        {
            "$limit": 5
        }
    ]

    results = api_logs.aggregate(pipeline)
    response = []
    for item in results:
        response.append({
            "source": item["_id"]["source"],
            "destination": item["_id"]["destination"],
            "search_count": item["count"]
        })

    return Response(response)