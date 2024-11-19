# Fetch
Fetch Backend Engineer Take Home Test by [@evanddunn](https://github.com/evanddunn)

## Context
The project provides an API with two endpoints both under the `receipts/` path:

- `/receipts/process`
  - Allowed methods: `POST`
  - Payload: Receipt JSON
  - Response: JSON containing an id for the receipt
    - ex: `{ "id": "cf09f96b-9244-4619-b026-9d92c93fbedc" }`
- `/receipts/{receipt_id/points` where `receipt_id` is a uuid provided by the `/process` endpoint
  - Allowed methods: `GET`
  - Response: A JSON object containing the number of points awarded according to the points rules defined below
    - ex. `{ "points": 31 }`
  - Rules: 
    1) One point for every alphanumeric character in the retailer name.
    2) 50 points if the total is a round dollar amount with no cents.
    3) 25 points if the total is a multiple of 0.25.
    4) 5 points for every two items on the receipt.
    5) If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
    6) 6 points if the day in the purchase date is odd.
    7) 10 points if the time of purchase is after 2:00pm and before 4:00pm.

## How to Run
The project is Dockerized so simply compose up and it will fire up and run.
### Steps

1) Run `docker compose up`  to build the instance and run the container.
2) Hit the API at `http://127.0.0.1:8000/receipts/process` with the tool of your choosing (Thunder Client, Postman, etc.) and start testing!

## Notes
The API has an extremely bare bones db model on it which simply saves a uuid and the complete json receipt data. This is connected to a SQLite instance. The DB will only be persistent as long as the image hasn't been removed. There is no set up required for this. Simply run the docker and Django will set up a db file. Run `docker compose down` when finished testing and everything will be removed. As the instructions said not to worry about persistent data, there was no need to hook up a Postgres database or anything of the like. Happy testing!
