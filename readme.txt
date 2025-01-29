Green taxi trip data has 12 incorrect rows:
Query: select * from green_taxi_trips gtt where date_part('year',lpep_pickup_datetime::date)!='2019';


Question 1. Understanding docker first run
Run docker with the python:3.12.8 image in an interactive mode, use the entrypoint bash.

What's the version of pip in the image?
Ans: pip 24.3.1 from /usr/local/lib/python3.12/site-packages/pip (python 3.12)

Question 2. Understanding Docker networking and docker-compose
Given the following docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?

services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin  

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data

Ans: postgres:5432

Question 3. Trip Segmentation Count
During the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive), how many trips, respectively, happened:

1.Up to 1 mile
Ans: 104,838
Query:
SELECT COUNT(*)
FROM public.green_taxi_trips
WHERE lpep_pickup_datetime >= '2019-10-01' AND lpep_pickup_datetime < '2019-11-01'
AND trip_distance <= 1;

2.In between 1 (exclusive) and 3 miles (inclusive)
Ans: 199,013
Query:
SELECT COUNT(*)
FROM public.green_taxi_trips
WHERE lpep_pickup_datetime >= '2019-10-01' AND lpep_pickup_datetime < '2019-11-01'
AND trip_distance > 1 AND trip_distance <= 3;

3.In between 3 (exclusive) and 7 miles (inclusive)
Ans: 109,645
Query:
SELECT COUNT(*)
FROM public.green_taxi_trips
WHERE lpep_pickup_datetime >= '2019-10-01' AND lpep_pickup_datetime < '2019-11-01'
AND trip_distance > 3 AND trip_distance <= 7;

4.In between 7 (exclusive) and 10 miles (inclusive).
Ans: 27,688
Query:
SELECT COUNT(*)
FROM public.green_taxi_trips
WHERE lpep_pickup_datetime >= '2019-10-01' AND lpep_pickup_datetime < '2019-11-01'
AND trip_distance > 7 AND trip_distance <= 10;

5.In between 10 (exclusive) and 20 miles (inclusive).
Ans: 1,000,000
Query:
SELECT COUNT(*)
FROM public.green_taxi_trips
WHERE lpep_pickup_datetime >= '2019-10-01' AND lpep_pickup_datetime < '2019-11-01'
AND trip_distance > 10 AND trip_distance <= 20;

6.Over 10 miles.
Ans:35,202
Query:
SELECT COUNT(*)
FROM public.green_taxi_trips
WHERE lpep_pickup_datetime >= '2019-10-01' AND lpep_pickup_datetime < '2019-11-01'
AND trip_distance > 10;

Question 4. Longest trip for each day
Which was the pick up day with the longest trip distance? Use the pick up time for your calculations.
2019-10-11
2019-10-24
2019-10-26
2019-10-31
Ans: 2019-10-31
Query:select lpep_pickup_datetime ,trip_distance from green_taxi_trips gtt 
where lpep_pickup_datetime::date='2019-10-11' 
or lpep_pickup_datetime='2019-10-24'
or lpep_pickup_datetime::date='2019-10-26' 
or lpep_pickup_datetime::date='2019-10-31' order by trip_distance desc limit 1;

Question 5. Three biggest pickup zones
Which were the top pickup locations with over 13,000 in total_amount (across all trips) for 2019-10-18?
Ans: East Harlem North	14587.039999999999
Query: select z."Zone" ,sum(fare_amount) fare_amount from green_taxi_trips gtt left join zones z on
gtt."PULocationID" =z."LocationID" 
where gtt.lpep_pickup_datetime::date='2019-10-18'
group by 1 
having sum(fare_amount)>13000;

Question 6. Largest tip
For the passengers picked up in October 2019 in the zone named "East Harlem North" which was the drop off zone that had the largest tip?
Ans: JFK Airport
Query: select * from zones z where "LocationID" =(
select "DOLocationID" from green_taxi_trips gtt left join zones z on
gtt."PULocationID" =z."LocationID"
where z."Zone"='East Harlem North'
order by tip_amount desc limit 1);

Question 7. Terraform Workflow
Which of the following sequences, respectively, describes the workflow for:

1. Downloading the provider plugins and setting up backend,
Ans: terraform init
2. Generating proposed changes and auto-executing the plan.
Ans: terraform run -auto-approve
3. Remove all resources managed by terraform.
Ans: terraform destroy
