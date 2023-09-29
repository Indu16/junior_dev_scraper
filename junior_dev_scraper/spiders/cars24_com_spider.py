import scrapy
import json
import re
import benedict
from w3lib.url import add_or_replace_parameter

# See https://www.cars24.com/ae/buy-used-cars-dubai/


class Car24ComSpider(scrapy.Spider):
    name = 'cars24_com_spider'
    custom_settings = {
        'FEEDS': { 'Output.csv': { 'format': 'csv',}}
    }
    # def parse(self, response):
    #     for cars in response.css("div._3IIl_._1xLfH"):
    #         year =cars.css("p._1i1E6 ::text").get()[:4]
    #         fuel=cars.css("img._3oX3Z ::attr(alt)").get().split(',')[-1][:-4]
    #         yield {
    #         "Model": cars.css("h3.RZ4T7 ::text").get(),
    #         "DeepUrl": cars.css("div._3IIl_._1xLfH a._1Lu5u ::attr(href)").get(),
    #         "Price": cars.css("span._7yds2 ::text").get(),
    #         "Engine size": cars.css("ul._3ZoHn li::text")[2].get(),
    #         "Mileage": cars.css("ul._3ZoHn li::text")[1].get(),
    #         "Fuel": fuel,
    #         "Year": year,
    #         }

    def start_requests(self):
        url = "https://listing-service.c24.tech/v2/vehicle?isSeoFilter=true&sf=city:DU&sf=gaId:1747585988.1695838047&size=25&spath=buy-used-cars-dubai&page=1&variant=filterV5"

    # Set the headers here. The important part is "application/json"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'X_country': 'AE',
            'X_vehicle_type': 'CAR'}

        yield scrapy.http.Request(url, headers=headers)

    def parse(self, response):
        parsedjson = json.loads(response.body)
        cars = parsedjson["results"]
        for car in cars:
            yield {
                "Make" : car["make"],
                "Model": car["model"],
                "Engine Size": car["engineSize"],
                "Year":car["year"],
                "Fuel":car["fuelType"],
                "Price":car["price"],
                "DeepUrl":car["shortInspectionReportUrl"],
                "Mileage":car["odometerReading"],
            }
