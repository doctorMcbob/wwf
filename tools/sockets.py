#python imports
import socket as so
import sys
import re

#database imports (sqlalchemy)
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

#app imports
from .views import URLS
from .http import parse_request, err_response


def run_server(ADDR, DATABASE_URL):
    """Very simple server script
    """

    engine = create_engine(DATABASE_URL)
    DBSession = scoped_session(
        sessionmaker(
            bind=engine,
            extension=ZopeTransactionExtension())
    )

    SERVERSOCK = so.socket(
        so.AF_INET, so.SOCK_STREAM, so.IPPROTO_IP
    )
    SERVERSOCK.setsockopt(so.SOL_SOCKET, so.SO_REUSEADDR, 1)

    SERVERSOCK.bind(ADDR)
    SERVERSOCK.listen(1)
    while True:
        # recieve request
        try:
            conn, addr = SERVERSOCK.accept()
            s, msg = "", True
            while msg:
                msg = conn.recv(1024)
                s += msg
                if len(msg) < 1024:
                    break
        # parse and complete request
            try:
                data = parse_request(s)
                resp = None
                for url in URLS:
                    if re.search(url[0], data["uri"]):
                        resp = url[1][data["method"]](
                            data, session=DBSession()
                        )
        # handle server errors
                if resp is None:
                    raise ValueError("404 Not Found")
            except Exception as e:
                resp = err_response(e)
        except KeyboardInterrupt:
            break

        # send response
        conn.sendall(resp)
        conn.close()
