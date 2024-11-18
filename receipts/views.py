import re
import uuid
import math
import datetime

from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

#! TODO: DELETE!
RECEIPTS = {
    "b43ac565-4874-46ca-93f4-e3c353f21c5d": {
        "retailer": "M&M Corner Market",
        "purchaseDate": "2022-03-20",
        "purchaseTime": "14:33",
        "items": [
            {"shortDescription": "Gatorade", "price": "2.25"},
            {"shortDescription": "Gatorade", "price": "2.25"},
            {"shortDescription": "Gatorade", "price": "2.25"},
            {"shortDescription": "Gatorade", "price": "2.25"},
        ],
        "total": "9.00",
    },
    "7b88308f-fef5-4d53-9b72-da1a0fd306d7": {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
            {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
            {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
            {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
            {"shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": "12.00"},
        ],
        "total": "35.35",
    },
}


class ProcessReceiptView(APIView):

    def post(self, request):
        receipt_id = uuid.uuid4()
        response = {"id": receipt_id}
        return Response(response)


class GetPointsView(APIView):

    def get(self, request, receipt_id):

        receipt = RECEIPTS.get(receipt_id)
        points = 0

        # Rule 1) One point for every alphanumeric character in the retailer name.
        matches = re.findall("[0-9a-zA-Z]", receipt["retailer"])
        points += len(matches)

        # Rule 2) 50 points if the total is a round dollar amount with no cents.
        total = float(receipt["total"])
        round_dollar = total.is_integer()
        if round_dollar:
            points += 50

        # Rule 3) 25 points if the total is a multiple of 0.25.
        if not total % 0.25:
            points += 25

        # Rule 4) 5 points for every two items on the receipt.
        items = receipt["items"]
        points += (5 * math.floor(len(items) / 2))
        
        # Rule 5) If the trimmed length of the item description is a multiple of 3,
        # multiply the price by 0.2 and round up to the nearest integer.
        # The result is the number of points earned.
        for item in items:
            stripped_item = item["shortDescription"].strip()
            if len(stripped_item) % 3 is 0:
                points_to_add = math.ceil(float(item["price"]) * 0.2)
                points += points_to_add

        # Rule 6) 6 points if the day in the purchase date is odd.
        day_of_purchase = datetime.datetime.strptime(
            f"{receipt["purchaseDate"]}:{receipt["purchaseTime"]}", "%Y-%m-%d:%H:%M"
        )
        is_odd = day_of_purchase.day % 2 is not 0
        if is_odd:
            points += 6

        # Rule 7) 10 points if the time of purchase is after 2:00pm(14:00) and before 4:00pm(16:00).
        if 14 <= day_of_purchase.hour < 16:
            points += 10


        return Response({"points": points})
