import cv2

cap = cv2.VideoCapture(0) # Canal donde se muestra la cámara
winName = 'IP_CAM' # Ventana donde abriremos la imagen

cv2.namedWindow(winName, cv2.WINDOW_AUTOSIZE)

while True:
    ret, frame = cap.read()
    
    if ret:
        # Dibujar líneas verticales
        for i in range(1, 6):
            x = int(frame.shape[1] / 6) * i
            cv2.line(frame, (x, 0), (x, frame.shape[0]), (0, 255, 255), 1)
        
        # Dibujar líneas horizontales
        for i in range(1, 6):
            y = int(frame.shape[0] / 6) * i
            cv2.line(frame, (0, y), (frame.shape[1], y), (0, 0, 255), 1)
        
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Aplicar desenfoque y detección de bordes
        blurred = cv2.medianBlur(frame_gray, 9)
        edges = cv2.Canny(blurred, threshold1=200, threshold2=120)
        
        # Encontrar contornos
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        
        # Dibujar los contornos en el frame original
        cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
        
        # Calcular el punto medio en la línea de en medio
         
        if len(contours) >= 2:
            cnt1 = contours[0]
            cnt2 = contours[1]
            M1 = cv2.moments(cnt1)
            M2 = cv2.moments(cnt2)
            if M1["m00"] != 0 and M2["m00"] != 0:
                cX1 = int(M1["m10"] / M1["m00"])
                cY1 = int(M1["m01"] / M1["m00"])
                cX2 = int(M2["m10"] / M2["m00"])
                cY2 = int(M2["m01"] / M2["m00"])
                
                # Calcular punto medio
                mid_point = (int((cX1 + cX2) / 2), int(frame.shape[0] / 2))
                
                # Dibujar un punto en la línea de en medio
                cv2.circle(frame, mid_point, 5, (0, 0, 255), 5)
        
        cv2.imshow(winName, frame)
        
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
