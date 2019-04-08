from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABcny8NtCA9sEKbqN1zQX-fjEDACBuhONRWvCC-aT0m2G0wRt1K6M1ORw5nwlj2_Nyw0wa_5ajHZBvG-cfVqlGIXe5MN75Khimlj2WpLHTkU3AB7ikrP9VvI3H53WsJSdE_2ciuYjQHy5zyz0KQkO6z-hK_xMtluckY2ODZkUVes3u5PU-bwz9tXSI9bREZyzZUHYiT'

def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()