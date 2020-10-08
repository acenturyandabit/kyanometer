# kyanometer
reveal hidden stores of wonder


## How to use with phone
1. Install the IP webcam app on the play store. It is by Pavel Khlebovich.
2. Connect your laptop to your phone hotspot.
2. Start the IP camera. (Scroll to the bottom and press 'Start server' in the IP webcam app.)
3. Change the link in `main.py` to `http://<IP address>:<port>/video`.
4. Make sure in `main.py` the `displayResult = CustomWebserver.output` rather than `displayResult=localDisplay`.
4. Run `main.py`.
5. On your phone,  go to `<your PC IP>:8038/`
6. You should see the output.
