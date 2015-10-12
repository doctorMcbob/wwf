from tools.sockets import run_server
import settings

# this needs to be here
import views

if __name__ == "__main__":
    run_server(
        ADDR=settings.ADDR, DATABASE_URL=settings.DATABASE_URL
    )
