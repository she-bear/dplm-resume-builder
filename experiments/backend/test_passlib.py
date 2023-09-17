from passlib.hash import pbkdf2_sha256

# хэширование пароля
hash = pbkdf2_sha256.hash("password")
print(hash)
# сравнение результата
print(pbkdf2_sha256.verify("password", hash))

# повторное хэширование одного и того же пароля...
hash_1 = pbkdf2_sha256.hash("secretword")
hash_2 = pbkdf2_sha256.hash("secretword")
# ... даёт разный результат
print(hash_1 == hash_2)

print("First password check: ", pbkdf2_sha256.verify("secretword", hash_1))
print("Second password check: ", pbkdf2_sha256.verify("secretword", hash_2))
