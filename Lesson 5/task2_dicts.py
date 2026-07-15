tutor_stats = {
    "name":"Іван Склянчук",
    "total_students":12,
    "active_groups":3,
    "rating":4.8
}
tutor_stats["total_students"] = tutor_stats["total_students"]+4
tutor_stats["subject"] = "Математика"
del tutor_stats["rating"]
print(f"""Профіль: {tutor_stats["name"]}.
Викладає: {tutor_stats["subject"]}.
Веде груп: {tutor_stats["active_groups"]}.
Загалом учнів: {tutor_stats["total_students"]}.""")