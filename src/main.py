from flask import Flask, request, jsonify

app = Flask(__name__)

CONSIDER_CO2_EMISSIONS = False
# You can change this variable according to the cost ou tCO2 you want to consider
CO2_COST = 7 if CONSIDER_CO2_EMISSIONS else 0


@app.route('/productionplan', methods=['POST'])
def production_plan():
    data = request.json
    load = data['load']
    fuels = data['fuels']
    powerplants = data['powerplants']

    # Calculate cost per MWh for each powerplant
    for plant in powerplants:
        if plant['type'] == 'windturbine':
            plant['cost'] = 0
            plant['pmax'] = plant['pmax'] * (fuels['wind(%)'] / 100)
        elif plant['type'] == 'gasfired':
            plant['cost'] = (fuels['gas(euro/MWh)'] + CO2_COST) / plant['efficiency']
        elif plant['type'] == 'turbojet':
            plant['cost'] = fuels['kerosine(euro/MWh)'] / plant['efficiency']

    # Sort powerplants by cost
    powerplants = sorted(powerplants, key=lambda x: x['cost'])

    # Allocate load to powerplants
    remaining_load = load
    result = []
    for plant in powerplants:
        if remaining_load <= 0:
            power = 0
        else:
            power = min(plant['pmax'], remaining_load)
            power = max(power, plant['pmin']) if remaining_load >= plant['pmin'] else 0

        remaining_load -= power
        result.append({"name": plant['name'], "p": round(power, 1)})

    # Ensure no overproduction and correct allocation
    if remaining_load > 0:
        for plant in reversed(result):
            if plant['p'] < [p['pmax'] for p in powerplants if p['name'] == plant['name']][0]:
                plant['p'] = round(plant['p'] + remaining_load, 1)
                break

    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
