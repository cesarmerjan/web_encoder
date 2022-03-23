# Web Encoder

Used to encode and decode data in a web-friendly format.

It's only uses building libraries, therefore, it has no external dependency.
It is also lightweight and thread-safe, which makes it ideal for use in services and microservices.

By default WebEncoder will try to compress the data.
If it manages to compress the data, the encoded data started with '.'.


## Typical usage example:


### Encode session
```python
web_encoder = WebEncoder()

session_id = "b801692b-135f-40ff-8f7e-016dc7748c45"
session = {"user_uuid": "67fa3e17-4672-4036-8184-7fbe4c097439"}
encoded_session = web_encoder.encode(json.dumps(session))

redis.set(session_id, encoded_session)
```

### Decode session
```python
web_encoder = WebEncoder()

session_id = "b801692b-135f-40ff-8f7e-016dc7748c45"
encoded_session = redis.get(session_id)
session = json.loads(web_encoder.decode(encoded_session))

```
