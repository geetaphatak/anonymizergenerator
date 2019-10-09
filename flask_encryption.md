## Running anonymizer application over HTTPS

For HTTP, the encryption and security functionality is implemented through the Transport Layer Security (TLS) protocol. TLS provides a simple and standard way to make any network communication channel secure.

To implement TLS encryption we need: 
- a server certificate that includes a public key and is signed by a CA
- a private key that goes with the public key included in the certificate

In general, when the client application establishes a connection with the server and requests an encrypted connection, the server responds back with its SSL Certificate. The certificate is the identification for the server and includes server name/domain. To verify that the information provided by the server is correct, the certificate is cryptographically signed by a certificate authority, or CA. If the client knows and trusts the CA, it will confirm that the certificate signature indeed comes from this entity, and with this the client can be certain that the server connected to is justified.

After verification of the certificate from the client, it creates an encryption key to use for the communication with the server. To make sure that this key is sent securely to the server, the client encrypts it using a public key that is included with the server certificate. The server is in possession of the private key that goes with that public key in the certificate. As a result, only the server is able to decrypt the package.  After the server receives the encryption key, all traffic is encrypted with the key that only the client and server are aware of.

### On-the-fly certificates

Flask supports the use of on-the-fly certificates. It's as simple as adding `ssl_context='adhoc'` to the `app.run()` call. As an example, you can see the below Flask application from the official documentation, with TLS encryption added:

```python
    from flask import Flask
    app = Flask(__name__)

    @app.route("/")
    def process_data():
        return "success"

    if __name__ == "__main__":
        app.run(ssl_context='adhoc')

```

Alternatively, you can also perform the above using Flask CLI if you are using a Flask 1.x release:

```
    flask run --cert=adhoc
```

In addition, to use ad hoc certificates with Flask, you need to install pyOpenSSL. pyOpenSSL is a high-level wrapper around a subset of the OpenSSL library.

```
    pip install pyopenssl
```

When you run the application script, you will notice that Flask indicates that it is running an https:// server:

```
 * Running on https://127.0.0.1:5000/ (Press CTRL+C to quit)
```

## Self-signed certificates

A self-signed certificate is one where the signature is generated using the private key that is associated with that same certificate. Web browsers and other HTTP clients come pre-configured with a list of known and trusted CAs, but obviously if you use a self-signed certificate the CA is not going to be known and validation will fail. That can happen with ad hoc certificate(s). If the web browser is unable to validate a server certificate, it will let you proceed and visit the site in question, but it will ensure that you are doing it at your own risk.

While self-signed certificates can be useful sometimes, the ad hoc certificates from Flask are not that great, because each time the server runs, a different certificate is generated on the fly through pyOpenSSL. When you are working with a self-signed certificate, it is better to have the same certificate used every time you launch your server, because that allows you to configure your browser to trust it, and that eliminates the security warnings.

You can generate self-signed certificates easily from the command line. All you need is to have openssl installed:

```
    openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

The above generates a new certificate in _cert.pem_ with its corresponding private key in _key.pem_, with a validity period of _365_ days.

```
    Generating a 4096 bit RSA private key
    ......................++
    .............++
    writing new private key to 'key.pem'
    -----
    You are about to be asked to enter information that will be incorporated
    into your certificate request.
    What you are about to enter is what is called a Distinguished Name or a DN.
    There are quite a few fields but you can leave some blank
    For some fields there will be a default value,
    If you enter '.', the field will be left blank.
    -----
    Country Name (2 letter code) [AU]:US
    State or Province Name (full name) [Some-State]:California
    Locality Name (eg, city) []:Los Anggeles
    Organization Name (eg, company) [Internet Widgits Pty Ltd]:Marlabs
    Organizational Unit Name (eg, section) []:
    Common Name (e.g. server FQDN or YOUR name) []:localhost
    Email Address []:
```

The new self-signed certificate can be utilized in Flask applications by setting the _ssl_context_ argument in _app.run()_ to a tuple with the filenames of the certificate and private key files:

```
    from flask import Flask
    app = Flask(__name__)

    @app.route("/")
    def hello():
        return "Hello World!"

    if __name__ == "__main__":
        app.run(ssl_context=('cert.pem', 'key.pem'))
```

Alternatively, you can add the `--cert` and `--key` options to the flask run command if you are using Flask 1.x or newer:

```
    flask run --cert=cert.pem --key=key.pem
```
