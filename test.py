import smtplib
import string
import random
import paramiko
import csv

# Путь к web-driver
EXE_PATH = 'chromedriver.exe'
# Логин и пароль от вашей почты
EMAIL = 'login@mail.ru'
PASSWORD = 'pass'

# Ввод данных пользователя
server_ip = '192.168.0.1'
username = 'admin'
password = 'password'

# Установление SSH-соединения
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(server_ip, username=username, password=password)

# Выполнение команды на сервере Mikrotik для получения списка пользователей
stdin, stdout, stderr = ssh.exec_command('/ppp secret print detail')
user_list = stdout.readlines()
user_list_array = str(user_list).split(r", '\r\n', ")
lenu = len(user_list_array)

# Парсинг данных и запись их в CSV-файл
with open('user_list.csv', 'w', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Number', 'Login', 'Email', 'Password', 'NewPassword'])

    for i in range(lenu):
        if 'X' not in user_list_array[i] and ';;;' in user_list_array[i]:
            user_number = user_list_array[i].split("'")[1].split(r'   ;;;')[0]
            user_mail = user_list_array[i].split(';;; ')[1].split(r'\r\n')[0]
            user_name = user_list_array[i].split('name="')[1].split('" service')[0]
            user_password = user_list_array[i].split('password="')[1].split('profile=')[0].split(r'" \r\n')[0]
            writer.writerow([user_number, user_name, user_mail, user_password, ''])



def pass_gen():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    size = random.randrange(11, 12)
    return ''.join(random.choice(chars) for x in range(size))


# Чтение данных из CSV-файла
with open('user_list.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    rows = list(reader)

# Генерация новых паролей и добавление их в столбец "NewPassword"
for row in rows:
    new_password = pass_gen()  # Здесь нужно реализовать функцию generate_new_password()
    row['NewPassword'] = new_password

# Обновление данных в CSV-файле
with open('user_list.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(rows)


def send_email(message):
    to_addr = user_mail
    from_addr = 'mail@gmail.com'
    passwords = 'password'
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(from_addr, passwords)
        server.sendmail(from_addr, to_addr, message)

        return "The message was completed"

    except Exception as _ex:
        return f"{_ex}\nПроверь почту или пароль"


def main():
    global user_mail, user_newpass_email, user_name_email
    for i in rows:
        user_name_email = i['Login']
        user_mail = i['Email']
        user_newpass_email = i['NewPassword']

        message = f'Vash login vpn{user_name_email}, vash parol vpn {user_newpass_email}'
        if True:
            ssh.exec_command(f'/ppp secret set password={user_newpass_email} {user_name_email}')
        else:
            print('ошибка в терминальной команде')
        print(send_email(message=message))


if __name__ == "__main__":
    main()

