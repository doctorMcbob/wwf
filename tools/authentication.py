from sqlalchemy.orm.exc import NoResultFound

class Cryptr(object):
    def __init__(self, secret):
        self.secret = secret
        self.letters = list(
            ("abcdefghijklmnopqrstuvwxyz"
             "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
             "0123456789-=!@#$%^&*()_+.,? ")
        )

    def encrypt(self, plaintext):
        crypted = ""
        for i, token in enumerate(plaintext):
            if token not in self.letters:
                raise ValueError(
                    "unaccepted token {}".format(token)
                )
            n = self.letters.index(token)
            n += self.letters.index(
                self.secret[i % len(self.secret)]
            )
            crypted += self.letters[n % len(self.letters)]
        return crypted

    def decrypt(self, crypted):
        decrypted = ""
        for i, token in enumerate(crypted):
            n = self.letters.index(token)
            n -= self.letters.index(self.secret[i % len(self.secret)])
            decrypted += self.letters[n % len(self.letters)]
        return decrypted


def is_authenticated(request, usermodel, cryptrobject):
    if "Authorization" in request["headers"]:
        info = request["headers"]["Authorization"].split(" ", 1)[0]
        info = crypterobject.decrypt(info)
        name, pswrd = info.split(":")
        try:
            user = usermodel.get_by_name(name)
            if user.password == pswrd:
                return True
        except NoResultFound:
            pass
    return False

