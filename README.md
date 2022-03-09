# METAR-API

API created in django for getting the METAR  report inf json format.
Read the SETUP_README.txt before running the app.

Sample METAR report:

    METAR VOHS 090300Z 18004KT 5000 HZ NSC 28/15 Q1017 NOSIG

JSON format API: 

```{
  "data": {
    "scode": "VOHS",
    "issued_on": "day 09 of the month at 03:00 GMT",
    "observation_type": null,
    "wind": {
      "direction": "180 degrees",
      "speed": "04 knots (5 mph)",
      "gusts": null,
      "variation": null
    },
    "visibility": "4 statute miles (5000 meters)",
    "runway_visual_range": null,
    "weather": "moderate haze on station",
    "clouds": "no significant clouds",
    "temp_and_dewpoint": "temperature: 28 C (83 F), dew point: 15 C (59 F)",
    "air_pressure": "1017 hPa",
    "last_observation": "2022/03/09 at 03:00 GMT"
  }
}```
