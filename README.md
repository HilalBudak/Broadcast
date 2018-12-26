Broadcast with Python

Python pyaudio ve cv2 kütüphaneleri kullanılarak görüntü ve ses yayını yapıldı.
Client-server mimarisi kullanıldı.
TCP protokolü kullanıldığı için görüntü iletiminde hafif duraksamalar yaşanmakta.


Kodları çalıştırmak için;

	python2.7 goruntu_server.py HOST PORT
	python2.7 goruntu_client.py HOST PORT
	
	python2.7 ses_server.py HOST PORT
	python2.7 ses_client.py HOST PORT
	
	python2.7 live_stream_server.py HOST PORT 1or0   --> 1 ile belirlediğiniz IP grubuna yayın yapabilirsiniz.
						         --> 0 ile public yayın yapabilirsiniz.
	python2.7 live_stream_client.py HOST PORT

Yayını yapan server olduğu için önce server kodunu çalıştırmanız gerekmekte.


