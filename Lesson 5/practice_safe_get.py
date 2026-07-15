payment_payload = {
    "transaction_id": 987654,
    "status": "success"
}
payment_payload = payment_payload.get("amount",0.0)
is_valid_amount = payment_payload["amount"] > 0
print(f"""Транзакція {payment_payload["transaction_id"]}.
Статус: {payment_payload["status"]}.
Отримана сума: {payment_payload["amount"]}.
Чи є сума валідною: {is_valid_amount}.""")