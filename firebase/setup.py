import os
from firebase_admin import initialize_app, auth, firestore, exceptions, credentials

# cred = {
#   "type": os.environ["TYPE"],
#   "project_id": os.environ["PROJECT_ID"],
#   "private_key_id": os.environ["PRIVATE_KEY_ID"],
#   "private_key": os.environ["PRIVATE_KEY"].replace('\\n', '\n'),
#   "client_email": os.environ["CLIENT_EMAIL"],
#   "client_id": os.environ["CLIENT_ID"],
#   "auth_uri": os.environ["AUTH_URI"],
#   "token_uri": os.environ["TOKEN_URI"],
#   "auth_provider_x509_cert_url": os.environ["AUTH_PROVIDER_X509_CERT_URL"],
#   "client_x509_cert_url": os.environ["CLIENT_X509_CERT_URL"],
# }


cred = {
  "type": "service_account",
  "project_id": "cendek-url",
  "private_key_id": "6c16973e221ab3ad587721d92d4cd69f97b45e2d",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDMtB2U2s9hZ9nu\n6vuFvVffph9A9+dnThD/xjfZSFzIwqokQth25uqfC9xvKcPVu/X91XZhuoBzrMq5\nmT/tdz0M0V8Fe64otpsT2d5oItOjdGaiONtcvD9Tw8qRf3cP29wh+NE2v+0r+2Ph\nsDqIUdcGQGR8CZuzi7z8/6IZloTka3+Y0Mm7cQJz0/TBesQsORk6weXGwIf3U9kS\nJjlpItwkxxzoSI7nCN7jjIVMZ6VlqbTfscU4mI+gMLJqbrzwIfz+DfLU7XNTYE4f\nhYXkcR1dS9NNbbtc6gUp0GtqkieVFetb2yldWYACsm7V8osPtJBrYV3yTuqkT4Qm\nDXfW2JV3AgMBAAECggEADSMqGtmIIao2lFzEU6r5LsNMkjDWywx5jtC72NgKDGBh\n5v3bQpZDTH3IYeH+TYNIoEfI1zDO+Z2HTS4GqkjSxDXTsVhkrvw5K6b53RkPGBhq\nVdLsUSFLtyaDo57Yl0327L85PhhHMmFp4ZwbxY/rCt2rFULQmU9Ii7wkPRwp3zbh\nhRj9rNWD5BRtIb2EzADTb0W8Li+DYoxjmyYLJSt8zVKuy/l5nZ26SZrMmbHQycQA\nLDHDcSNOmqWOLwMu2kwSaTTP7Wh9fxSdKWmQZJmZYMAZm0+VOHUGLtCbtdQJOpQV\nL3bUYbyX36YPthqIYTQ60dxNd2oCTY0u5pzn73IbYQKBgQDyXJNRlZBPplck75tO\n6FsuBiZ7szxZGSB7yOKmgX0HD8TlnOQioaCQSsT4qfan94AR+1NXd8CJQwLMFCFt\nwJqgs7Yb9+BZYOeXDAbQptnKD0TqCkzhIFVRrpEgdiNRLulCTlyp8arFpO2furT7\nSIWTozmPavBY7NMk16rkj1k1zwKBgQDYOQtE6PCZ31zYNYfmoCltFhppt0NToH8x\nfcBUgTvOdZKU3ZMSH7X6J/2V2ySDe0L1x2abWPY61TI7RUxX+18lbwgJXk3OnzNv\nfy6+HfEK2olDYQBwkmLfzR+7h3/QwxjVJZiOuWjBp8j8n6s2Mz5S9jkiLNVlT81q\n4g5tCM232QKBgHUk8/wCG7+z+fkba2knfDLxvBYcWzYBpCbQwWSTwBfyskv9mnN2\nxgIYcb5zgIpNYfTPEsh7VG/EGQ0FSecfql20n3hDRohNA4OJx52AmFJHMRsioWhL\nVZHmm7UiBQ4Pa6Wl9Lob2lwvzL9g4mt28UGcKo08tjF1PtVW/P3+n7MXAoGBAJ0a\nhYeiQP9sfcdSzdXSVYc/Yh2h3LdsjD5nglFkPRI79y9W9z9Z7x095VD3E0a9Tt/J\n7FG/h9kjgwXxyhC7QlyumgZEkQAqSHMg09OrabJbKxTb7DffBRxbrEzTnRkQSIDG\nelxpdyYORUjYsswE26nn4YdlT//2xeh9K8IpfV+xAoGASBdHzivwPnEo+NTbY/IS\nxZycu8QxniOHj/n/ZthXAdlFtb9bxmcHSlyAIiBrGSppXrfFcb0i17L2wG9mrFT5\nTAJu4XmkGtzE640Hpfux0fKWJW5rJjF4Q4iVRdWiIQlRtH6xGBua9eqMFbcfLMZh\nIMdWIN1sBbMymf6TEv1V1FM=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-djz7d@cendek-url.iam.gserviceaccount.com",
  "client_id": "113193008036722300371",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-djz7d%40cendek-url.iam.gserviceaccount.com"
}


initialize_app(credentials.Certificate(cred))
db = firestore.client()