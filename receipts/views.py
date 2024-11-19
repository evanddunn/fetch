"""API Views for Receipts app"""

import re
import math
import datetime
from urllib import response

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Receipt

class ProcessReceiptView(APIView):
    """Process Receipt API View"""

    def post(self, request):
        """Take in receipt JSON, save item, generate and return items uuid"""

        receipt, created = Receipt.objects.get_or_create(data=request.data)
        response = {"id": receipt.uuid}
        return Response(response)


class GetPointsView(APIView):

    def get(self, request, receipt_id):
        """Take receipt id query param, calculate and return items points"""

        receipt = Receipt.objects.get(uuid=receipt_id).data  # Get Receipt JSON data
        points = 0

        # Rule 1) One point for every alphanumeric character in the retailer name.
        matches = re.findall("[0-9a-zA-Z]", receipt["retailer"])  # Match all alphanumeric chars with regex
        points += len(matches)

        # Rule 2) 50 points if the total is a round dollar amount with no cents.
        total = float(receipt["total"])
        round_dollar = total.is_integer()  
        if round_dollar:  # Only add points if total is an integer
            points += 50

        # Rule 3) 25 points if the total is a multiple of 0.25.
        if not total % 0.25: # Only add points if total is multiple of .25 (ends in .00, .25, .50, .75)
            points += 25

        # Rule 4) 5 points for every two items on the receipt.
        items = receipt["items"]
        points += (5 * math.floor(len(items) / 2))  # 5 points for every 2 items rounding down (i.e. 1 item is 0 points)
        
        # Rule 5) If the trimmed length of the item description is a multiple of 3,
        # multiply the price by 0.2 and round up to the nearest integer.
        # The result is the number of points earned.
        for item in items:
            stripped_item = item["shortDescription"].strip()  # Trim whitespace
            if len(stripped_item) % 3 is 0:  # Only add points if len of trimmed string is divisible by 3
                points_to_add = math.ceil(float(item["price"]) * 0.2)  # Add the num of points equal to price * .2 rounded up to whole int
                points += points_to_add

        # Rule 6) 6 points if the day in the purchase date is odd.
        day_of_purchase = datetime.datetime.strptime(
            f"{receipt["purchaseDate"]}:{receipt["purchaseTime"]}", "%Y-%m-%d:%H:%M"
        )  # Turn datetime string into datetime object
        is_odd = day_of_purchase.day % 2 is not 0
        if is_odd:  # Only add points if day is odd
            points += 6

        # Rule 7) 10 points if the time of purchase is after 2:00pm(14:00) and before 4:00pm(16:00).
        if 14 <= day_of_purchase.hour < 16:  # Only add points if hour is between 14 and 16 inclusive of 14 (i.e. 2:00pm-3:59pm)
            points += 10


        return Response({"points": points})
