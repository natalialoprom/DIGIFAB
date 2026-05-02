from flask import Flask, request
import board
import busio
import digitalio
from adafruit_epd.ssd1680 import Adafruit_SSD1680
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

app = Flask(__name__)

# -----------------------------
# E-INK SETUP
# -----------------------------
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D22)
rst = digitalio.DigitalInOut(board.D27)
busy = digitalio.DigitalInOut(board.D17)

display = Adafruit_SSD1680(
    122,
    250,
    spi,
    cs_pin=ecs,
    dc_pin=dc,
    sramcs_pin=None,
    rst_pin=rst,
    busy_pin=busy,
)

display.rotation = 1

try:
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
except:
    font_small = ImageFont.load_default()
    font_medium = ImageFont.load_default()
    font_large = ImageFont.load_default()

# -----------------------------
# STORE DATA
# -----------------------------
products = {
    "Tomatoes": {
        "status": "Waiting",
        "price": "29.90 NOK",
        "temp": "25.0C",
        "hum": "45",
        "gas": "38.5K",
        "live": True,
        "updated": "Never",
        "category": "Fresh Produce"
    },
    "Bananas": {
        "status": "Use soon",
        "price": "24.90 NOK",
        "temp": "23.8C",
        "hum": "58",
        "gas": "31.2K",
        "live": False,
        "updated": "Simulated",
        "category": "Fresh Produce"
    },
    "Apples": {
        "status": "Fresh",
        "price": "27.50 NOK",
        "temp": "22.5C",
        "hum": "49",
        "gas": "42.0K",
        "live": False,
        "updated": "Simulated",
        "category": "Fresh Produce"
    },
    "Oranges": {
        "status": "Discount",
        "price": "18.90 NOK",
        "temp": "24.3C",
        "hum": "67",
        "gas": "19.8K",
        "live": False,
        "updated": "Simulated",
        "category": "Fresh Produce"
    }
}

history = []

# -----------------------------
# HELPERS
# -----------------------------
def status_color(status):
    status = status.lower()
    if status == "fresh":
        return "#2e7d32"
    elif status == "use soon":
        return "#f9a825"
    elif status == "discount":
        return "#c62828"
    return "#546e7a"

def status_bg(status):
    status = status.lower()
    if status == "fresh":
        return "#e8f5e9"
    elif status == "use soon":
        return "#fff8e1"
    elif status == "discount":
        return "#ffebee"
    return "#eceff1"

def draw_screen(product, status, price, temp="", hum="", gas=""):
    image = Image.new("L", (250, 122), 255)
    draw = ImageDraw.Draw(image)

    draw.text((10, 8), product.upper(), font=font_medium, fill=0)
    draw.text((10, 35), status.upper(), font=font_medium, fill=0)
    draw.text((10, 68), price, font=font_large, fill=0)

    footer = f"T:{temp}  H:{hum}  G:{gas}"
    draw.text((10, 102), footer, font=font_small, fill=0)

    display.image(image)
    display.display()

def update_product(product, status, price, temp, hum, gas, live=False):
    now = datetime.now().strftime("%H:%M:%S")

    if product not in products:
        products[product] = {
            "status": status,
            "price": price,
            "temp": temp,
            "hum": hum,
            "gas": gas,
            "live": live,
            "updated": now,
            "category": "Fresh Produce"
        }
    else:
        products[product]["status"] = status
        products[product]["price"] = price
        products[product]["temp"] = temp
        products[product]["hum"] = hum
        products[product]["gas"] = gas
        products[product]["live"] = live
        products[product]["updated"] = now

    history.append({
        "time": now,
        "product": product,
        "status": status,
        "price": price
    })

def render_header(title, subtitle=""):
    return f"""
    <div style="
        background: linear-gradient(135deg, #1b5e20, #43a047);
        color: white;
        padding: 28px 22px;
        border-radius: 20px;
        margin-bottom: 20px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.12);
    ">
        <div style="font-size: 0.9rem; opacity: 0.9; letter-spacing: 0.05em;">SMART FRESH MARKET</div>
        <h1 style="margin: 8px 0 8px 0; font-size: 2rem;">{title}</h1>
        <p style="margin: 0; opacity: 0.95;">{subtitle}</p>
    </div>
    """

def render_nav():
    return """
    <div style="margin-bottom: 20px;">
      <a href="/store" style="margin-right: 14px;">Storefront</a>
      <a href="/dashboard" style="margin-right: 14px;">Operations Dashboard</a>
      <a href="/offers" style="margin-right: 14px;">Offers</a>
      <a href="/history">History</a>
    </div>
    """

# -----------------------------
# ROUTES
# -----------------------------
@app.route("/")
@app.route("/store")
def store():
    featured = ""
    for name, data in products.items():
        if data["status"] in ["Use soon", "Discount"]:
            featured += f"""
            <div style="
                background:white;
                border-radius:18px;
                padding:18px;
                margin-bottom:16px;
                box-shadow:0 3px 12px rgba(0,0,0,0.08);
                border:1px solid #eee;
            ">
                <div style="font-size:0.8rem; color:#666; margin-bottom:6px;">{data['category']}</div>
                <h2 style="margin:0 0 10px 0;">{name}</h2>
                <div style="
                    display:inline-block;
                    padding:8px 14px;
                    border-radius:999px;
                    color:{status_color(data['status'])};
                    background:{status_bg(data['status'])};
                    font-weight:bold;
                    margin-bottom:10px;
                ">
                    {data['status']}
                </div>
                <h3 style="font-size:2rem; margin:8px 0;">{data['price']}</h3>
                <p style="color:#555; margin:0;">Promoted to reduce food waste and support responsible consumption.</p>
            </div>
            """

    if not featured:
        featured = """
        <div style="background:white; border-radius:18px; padding:18px; box-shadow:0 3px 12px rgba(0,0,0,0.08);">
            <p style="margin:0;">No active freshness-based promotions right now.</p>
        </div>
        """

    return f"""
    <html>
    <head>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Smart Fresh Market</title>
    </head>
    <body style="font-family:Arial,sans-serif; margin:0; background:#f6f7f8; color:#1f1f1f;">
      <div style="max-width:760px; margin:0 auto; padding:20px;">
        {render_header("Today's Freshness Offers", "A smart retail prototype for freshness-aware discounts and reduced food waste.")}
        {render_nav()}

        <div style="
            background:#e8f5e9;
            border-left:6px solid #2e7d32;
            padding:16px;
            border-radius:12px;
            margin-bottom:20px;
        ">
          <strong>Why these offers matter:</strong><br>
          Products marked as <em>Use soon</em> or <em>Discount</em> are promoted to encourage timely sale and reduce unnecessary waste.
        </div>

        <h2 style="margin-top:0;">Featured Offers</h2>
        {featured}
      </div>
    </body>
    </html>
    """

@app.route("/dashboard")
def dashboard():
    cards = ""
    for name, data in products.items():
        live_badge = ""
        if data["live"]:
            live_badge = """
            <span style="
              background:#1565c0;
              color:white;
              padding:4px 10px;
              border-radius:999px;
              font-size:0.75rem;
              font-weight:bold;
              margin-left:8px;
            ">LIVE SHELF</span>
            """

        cards += f"""
        <div style="
            background:white;
            border-radius:18px;
            padding:18px;
            margin-bottom:16px;
            box-shadow:0 3px 12px rgba(0,0,0,0.08);
            border:1px solid #eee;
        ">
            <div style="font-size:0.8rem; color:#666; margin-bottom:6px;">{data['category']}</div>
            <h2 style="margin:0 0 10px 0;">{name}{live_badge}</h2>

            <div style="
                display:inline-block;
                padding:8px 14px;
                border-radius:999px;
                color:{status_color(data['status'])};
                background:{status_bg(data['status'])};
                font-weight:bold;
                margin-bottom:12px;
            ">
                {data['status']}
            </div>

            <h3 style="font-size:2rem; margin:8px 0;">{data['price']}</h3>

            <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:12px;">
              <div><strong>Temperature:</strong> {data['temp']}</div>
              <div><strong>Humidity:</strong> {data['hum']}</div>
              <div><strong>Gas:</strong> {data['gas']}</div>
              <div><strong>Updated:</strong> {data['updated']}</div>
            </div>
        </div>
        """

    return f"""
    <html>
    <head>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Operations Dashboard</title>
    </head>
    <body style="font-family:Arial,sans-serif; margin:0; background:#f6f7f8; color:#1f1f1f;">
      <div style="max-width:760px; margin:0 auto; padding:20px;">
        {render_header("Operations Dashboard", "Live and simulated freshness states for monitored products.")}
        {render_nav()}
        {cards}
      </div>
    </body>
    </html>
    """

@app.route("/offers")
def offers():
    offer_cards = ""
    for name, data in products.items():
        if data["status"] in ["Use soon", "Discount"]:
            offer_cards += f"""
            <div style="
                background:white;
                border-radius:18px;
                padding:18px;
                margin-bottom:16px;
                box-shadow:0 3px 12px rgba(0,0,0,0.08);
                border:1px solid #eee;
            ">
                <div style="font-size:0.8rem; color:#666; margin-bottom:6px;">{data['category']}</div>
                <h2 style="margin:0 0 10px 0;">{name}</h2>
                <div style="
                    display:inline-block;
                    padding:8px 14px;
                    border-radius:999px;
                    color:{status_color(data['status'])};
                    background:{status_bg(data['status'])};
                    font-weight:bold;
                    margin-bottom:12px;
                ">
                    {data['status']}
                </div>
                <h3 style="font-size:2rem; margin:8px 0;">{data['price']}</h3>
                <p style="margin:0 0 8px 0;"><strong>Temperature:</strong> {data['temp']}</p>
                <p style="margin:0 0 8px 0;"><strong>Humidity:</strong> {data['hum']}</p>
                <p style="margin:0;"><strong>Gas:</strong> {data['gas']}</p>
            </div>
            """

    if not offer_cards:
        offer_cards = """
        <div style="background:white; border-radius:18px; padding:18px; box-shadow:0 3px 12px rgba(0,0,0,0.08);">
            <p style="margin:0;">No active offers right now.</p>
        </div>
        """

    return f"""
    <html>
    <head>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Offers</title>
    </head>
    <body style="font-family:Arial,sans-serif; margin:0; background:#f6f7f8; color:#1f1f1f;">
      <div style="max-width:760px; margin:0 auto; padding:20px;">
        {render_header("Active Offers", "Products promoted due to freshness-aware monitoring.")}
        {render_nav()}
        {offer_cards}
      </div>
    </body>
    </html>
    """

@app.route("/history")
def show_history():
    rows = ""
    for item in reversed(history[-20:]):
        rows += f"""
        <tr>
          <td style="padding:10px; border-bottom:1px solid #ddd;">{item['time']}</td>
          <td style="padding:10px; border-bottom:1px solid #ddd;">{item['product']}</td>
          <td style="padding:10px; border-bottom:1px solid #ddd;">{item['status']}</td>
          <td style="padding:10px; border-bottom:1px solid #ddd;">{item['price']}</td>
        </tr>
        """

    if not rows:
        rows = """
        <tr>
          <td colspan="4" style="padding:10px;">No history yet.</td>
        </tr>
        """

    return f"""
    <html>
    <head>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>History</title>
    </head>
    <body style="font-family:Arial,sans-serif; margin:0; background:#f6f7f8; color:#1f1f1f;">
      <div style="max-width:860px; margin:0 auto; padding:20px;">
        {render_header("Update History", "Recent changes in freshness state and pricing.")}
        {render_nav()}
        <div style="background:white; border-radius:18px; overflow:hidden; box-shadow:0 3px 12px rgba(0,0,0,0.08); border:1px solid #eee;">
          <table style="width:100%; border-collapse:collapse;">
            <thead style="background:#1b5e20; color:white;">
              <tr>
                <th style="padding:12px; text-align:left;">Time</th>
                <th style="padding:12px; text-align:left;">Product</th>
                <th style="padding:12px; text-align:left;">Status</th>
                <th style="padding:12px; text-align:left;">Price</th>
              </tr>
            </thead>
            <tbody>
              {rows}
            </tbody>
          </table>
        </div>
      </div>
    </body>
    </html>
    """

@app.route("/update", methods=["GET"])
def update():
    product = request.args.get("product", "Tomatoes")
    status = request.args.get("status", "Fresh")
    price = request.args.get("price", "29.90 NOK")
    temp = request.args.get("temp", "")
    hum = request.args.get("hum", "")
    gas = request.args.get("gas", "")

    update_product(product, status, price, temp, hum, gas, live=True)
    draw_screen(product, status, price, temp, hum, gas)

    return "OK\n"

if __name__ == "__main__":
    first_product = "Tomatoes"
    draw_screen(
        first_product,
        products[first_product]["status"],
        products[first_product]["price"],
        products[first_product]["temp"],
        products[first_product]["hum"],
        products[first_product]["gas"]
    )
    app.run(host="0.0.0.0", port=5000)