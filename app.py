from flask import Flask, render_template, request, jsonify
import threading
import time
import logging

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Sistema de Energia
class EnergySystem:
    def __init__(self):
        self.devices = []  # Lista dinâmica de dispositivos
        self.company_rate = 0.5  # R$/kWh
        self.solar_rate = 0.1  # R$/kWh
        self.current_source = "Companhia Elétrica"
        self.total_consumption = 0
        self.is_running = False
        self.thread = None  # Thread para simulação

    def calculate_consumption(self):
        """Calcula o consumo total com base nos dispositivos."""
        self.total_consumption = sum(
            d["power"] * d["usage_hours"] / 1000 for d in self.devices
        )

    def switch_source(self):
        """Alterna entre a fonte de energia solar e da companhia elétrica."""
        if self.company_rate > self.solar_rate:
            self.current_source = "Energia Solar"
        else:
            self.current_source = "Companhia Elétrica"

    def simulate_real_time(self):
        """Simula o consumo em tempo real, alternando fontes e calculando consumo."""
        while self.is_running:
            self.calculate_consumption()
            self.switch_source()
            logging.debug(f"Consumo Total: {self.total_consumption} kWh")
            logging.debug(f"Fonte Atual: {self.current_source}")
            time.sleep(2)

    def start_simulation(self):
        """Inicia a simulação em uma nova thread."""
        if not self.is_running:
            self.is_running = True
            if self.thread and self.thread.is_alive():
                logging.warning("Thread já está em execução!")
                return
            self.thread = threading.Thread(target=self.simulate_real_time)
            self.thread.daemon = True
            self.thread.start()

    def stop_simulation(self):
        """Para a simulação e aguarda a thread terminar."""
        self.is_running = False
        if self.thread and self.thread.is_alive():
            self.thread.join()
            self.thread = None


# Instância do sistema de energia
system = EnergySystem()


@app.route("/")
def index():
    """Renderiza a página principal."""
    return render_template("index.html")


@app.route("/api/get_data", methods=["GET"])
def get_data():
    """Retorna os dados do sistema em tempo real."""
    data = {
        "total_consumption": system.total_consumption,
        "current_source": system.current_source,
        "devices": system.devices,
        "company_rate": system.company_rate,
        "solar_rate": system.solar_rate,
    }
    return jsonify(data)


@app.route("/api/add_device", methods=["POST"])
def add_device():
    """Adiciona um dispositivo ao sistema."""
    logging.debug("Recebendo solicitação para adicionar dispositivo.")
    device = request.json
    if not device:
        return jsonify({"status": "error", "message": "Dados inválidos"}), 400

    name = device.get("name")
    power = device.get("power")
    usage_hours = device.get("usage_hours")

    if not name or not isinstance(power, (int, float)) or not isinstance(usage_hours, (int, float)):
        return jsonify({"status": "error", "message": "Dados do dispositivo inválidos"}), 400

    system.devices.append({"name": name, "power": power, "usage_hours": usage_hours})
    return jsonify({"status": "success", "message": "Dispositivo adicionado"})


@app.route("/api/remove_device", methods=["POST"])
def remove_device():
    """Remove um dispositivo do sistema."""
    logging.debug("Recebendo solicitação para remover dispositivo.")
    device_name = request.json.get("name")
    if not device_name:
        return jsonify({"status": "error", "message": "Nome do dispositivo não fornecido"}), 400

    system.devices = [d for d in system.devices if d["name"] != device_name]
    return jsonify({"status": "success", "message": "Dispositivo removido"})


@app.route("/api/update_rates", methods=["POST"])
def update_rates():
    """Atualiza as tarifas de energia."""
    logging.debug("Recebendo solicitação para atualizar tarifas.")
    rates = request.json
    if not rates:
        return jsonify({"status": "error", "message": "Dados inválidos"}), 400

    company_rate = rates.get("company_rate")
    solar_rate = rates.get("solar_rate")

    if not isinstance(company_rate, (int, float)) or not isinstance(solar_rate, (int, float)) or company_rate <= 0 or solar_rate <= 0:
        return jsonify({"status": "error", "message": "Tarifas inválidas"}), 400

    system.company_rate = company_rate
    system.solar_rate = solar_rate
    return jsonify({"status": "success", "message": "Tarifas atualizadas"})


@app.route("/api/start", methods=["POST"])
def start():
    """Inicia a simulação em tempo real."""
    if system.is_running:
        return jsonify({"status": "error", "message": "Simulação já está em execução"}), 400
    system.start_simulation()
    return jsonify({"status": "success", "message": "Simulação iniciada"})


@app.route("/api/stop", methods=["POST"])
def stop():
    """Para a simulação em tempo real."""
    if not system.is_running:
        return jsonify({"status": "error", "message": "Simulação não está em execução"}), 400
    system.stop_simulation()
    return jsonify({"status": "success", "message": "Simulação parada"})


if __name__ == "__main__":
    app.run(debug=True)
