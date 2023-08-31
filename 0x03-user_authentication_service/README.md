## 0x03. User authentication service

### Start by running the server using `python3 app.py`

### Adding a user 
A user can be add by sending a post request `curl -XPOST localhost:5000/users -d 'email=bob@me.com' -d 'password=mySuperPwd'`
If the user is successfully created a json message `{"email":"bob@me.com","message":"user created"}` is seen, but if the user exit the message `{"message":"email already registered"}` with a response code of `400` is seen.
