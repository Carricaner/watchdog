from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

raw = "123"
encode = pwd_context.hash(raw)
print(encode)
print(pwd_context.verify(raw, encode))

