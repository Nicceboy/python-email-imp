from flask import Flask, render_template, request, send_file
from flask_qrcode import QRcode
from mailsender import MailSender



app = Flask(__name__)
qrcode = QRcode(app)

@app.route("/")
def template_test():
    return render_template('template.html', name="You", qr_string='https://www.youtube.com/watch?v=RmqPfLWe8G0')


@app.route('/template', methods=['GET'])
def setTemplate():
    # please get /template?name=<name>&qr_code=<qr_code>
    name = request.args.get('name', '')
    qr_code = request.args.get('qr_code', '')
    return  render_template('template.html', name=name, qr_string=qr_code)

@app.route('/qrcode', methods=['GET'])
def get_qrcode():
    # please get /qrcode?data=<qrcode_data>
    data = request.args.get('data', '')
    return send_file(
        qrcode(data, mode='raw'),
        mimetype='image/png'
    )
@app.route('/sendtestmail', methods=['GET'])
def sendMail():
    option = request.args.get('arewesending', '')
    if option == 'YES':

        mail = MailSender('Example Man', 'example@example.com', 'Example to turn in QR code')

        mail.createMessage()
        mail.sendMail()
        return  render_template('successfullmail.txt')
    else:
        return  render_template('mailerror.txt')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
