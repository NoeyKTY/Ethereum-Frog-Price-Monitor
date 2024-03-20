import requests
import time

# สร้าง Token ของ LINE Notify จาก https://notify-bot.line.me/my/
LINE_NOTIFY_TOKEN = 'YOUR_LINE_NOTIFY_TOKEN'

# ลิงก์ API สำหรับดึงข้อมูลราคา NFT จากตลาด
NFT_API_URL = 'YOUR_NFT_API_URL'

# ฟังก์ชันสำหรับส่งข้อความแจ้งเตือนผ่าน LINE Notify
def send_line_notification(message):
    headers = {
        'Authorization': f'Bearer {LINE_NOTIFY_TOKEN}',
    }
    payload = {'message': message}
    requests.post('https://notify-api.line.me/api/notify', headers=headers, data=payload)

# ฟังก์ชันสำหรับดึงข้อมูลราคา NFT
def get_nft_price():
    try:
        response = requests.get(NFT_API_URL)
        data = response.json()
        nft_price = data['price']  # ปรับตามโครงสร้างข้อมูลจริง
        return nft_price
    except Exception as e:
        print("Error fetching NFT price:", e)
        return None

# วงจรหลักสำหรับตรวจสอบและแจ้งเตือนเมื่อมีการเปลี่ยนแปลงในราคา NFT
def main():
    previous_price = None

    while True:
        current_price = get_nft_price()

        if current_price is not None:
            if previous_price is None:
                previous_price = current_price
                print("Initial price:", current_price)
            elif current_price != previous_price:
                price_change = current_price - previous_price
                message = f"NFT ราคาใหม่: {current_price} ({'เพิ่มขึ้น' if price_change > 0 else 'ลดลง'} {abs(price_change)})"
                send_line_notification(message)
                previous_price = current_price
                print(message)

        time.sleep(60)  # ตรวจสอบราคาทุกๆ 1 นาที

if __name__ == "__main__":
    main()
