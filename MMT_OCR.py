import fitz  
import easyocr
import os
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog
import csv

global Nserie, Nof, Mac

def resource_path(relative_path):
    """Get the absolute path to a resource, works for PyInstaller."""
    try:
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def pdf_to_text(pdf_path, output_dir):
    global Nserie, Nof, Mac
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Ruta a los modelos dentro del ejecutable
    model_storage_directory = resource_path('model')

    # Inicializar EasyOCR con la ruta 
    reader = easyocr.Reader(['en'], model_storage_directory=model_storage_directory)
    all_text = []

    # Case 1: 4 Pages
    if len(pdf_document) == 4:
        for page_number in range(len(pdf_document)):
            # Render page to an image with higher resolution
            page = pdf_document[page_number]
            zoom = 4.0  # Increase this value for higher resolution (e.g., 2.0 = 200% zoom)
            adjust = 4
            matrix = fitz.Matrix(zoom*adjust, zoom*adjust)  # Apply zoom to both x and y axes
            pix = page.get_pixmap(matrix=matrix)  # Render the page with the specified matrix

            # Convert pixmap to numpy array for OpenCV processing
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)

            # Display the preprocessed image using matplotlib 
            """
            plt.imshow(img, cmap='gray')
            plt.title(f'Preprocessed Image - Page {page_number + 1}, Rect {page_number + 1}')
            plt.axis('off')
            plt.show()
            """
            
            # Define the list of rectangles for the current page
            rectangles = []
            if page_number == 0: 
                #continue #BORRAR!!!!
                # Add multiple rectangles for page 1
                rectangles.append((int(300 * adjust), int(270 * adjust), int(7060), int(1451)))  # INIT NSERIE NOF MACHINE
                #rectangles.append((int(500 * adjust), int(3070 * adjust), int(2260 * adjust), int(3210 * adjust)))  # Rectangle 2 Tabla completa
                rectangles.append((int(500 * adjust), int(3080 * adjust), int(615 * adjust), int(3210 * adjust)))  # Q FA
                rectangles.append((int(850 * adjust), int(3075 * adjust), int(1320 * adjust), int(3210 * adjust)))  # #FA
                rectangles.append((int(1440 * adjust), int(3075 * adjust), int(1910 * adjust), int(3210 * adjust)))  # #FNA
                rectangles.append((int(2150 * adjust), int(3080 * adjust), int(2260 * adjust), int(3210 * adjust)))  # Q FNA
                
            elif page_number == 1:
                #rectangles.append((int(125 * zoom), int(768 * zoom), int(565 * zoom), int(790 * zoom)))  # Rectangle 1 Complete Table
                rectangles.append((int(2002), int(12297), int(2464), int(12654)))  # QFA
                rectangles.append((int(850 * adjust), int(3075 * adjust), int(1320 * adjust), int(3200 * adjust)))  # FA
                rectangles.append((int(1440 * adjust), int(3075 * adjust), int(1910 * adjust), int(3200 * adjust)))  # FNAa
                rectangles.append((int(8595), int(12292), int(9067), int(12653))) # QFNA
                #rectangles.append((int(125 * zoom), int(768 * zoom), int(565 * zoom), int(790 * zoom)))  # Rectangle 2 Complete Table
                
            elif page_number == 2:
                print(f"Skipping page {page_number + 1}")
                continue
            
            elif page_number == 3:
                rectangles.append((int(720 * adjust), int(545 * adjust), int(940 * adjust), int(590 * adjust)))  # Exz
                rectangles.append((int(1600 * adjust), int(1100 * adjust), int(1820 * adjust), int(1150 * adjust)))  # Fu1
                rectangles.append((int(1600 * adjust), int(1665 * adjust), int(1820 * adjust), int(1710 * adjust)))  # FU2
                rectangles.append((int(1160 * adjust), int(2170 * adjust), int(1380 * adjust), int(2230 * adjust)))  # FP1I
                rectangles.append((int(1600 * adjust), int(2170 * adjust), int(1820 * adjust), int(2230 * adjust)))  # FP1D
                rectangles.append((int(1160 * adjust), int(2690 * adjust), int(1380 * adjust), int(2740 * adjust)))  # FP2I
                rectangles.append((int(1600 * adjust), int(2690 * adjust), int(1820 * adjust), int(2740 * adjust)))  # FP2D
                rectangles.append((int(1600 * adjust), int(3200 * adjust), int(1820 * adjust), int(3250 * adjust)))  # FR

            # Process each rectangle
            for rect_idx, (x1, y1, x2, y2) in enumerate(rectangles):
                # Crop the image using the defined coordinates
                cropped_img = img[y1:y2, x1:x2]

                # Convert the cropped image to grayscale
                gray_cropped_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)

                # Preprocess the image 
                preprocessed_img = gray_cropped_img
                
                # Save the preprocessed image
                cropped_image_path = os.path.join(output_dir, f'preprocessed_page_{page_number + 1}_rect_{rect_idx + 1}.jpg')
                cv2.imwrite(cropped_image_path, preprocessed_img)

                # Extract text from cropped image and Indexing data ------------------------>>>>>>>
                text = reader.readtext(cropped_image_path, detail=0)
                print(text)
                
                # Display the preprocessed image using matplotlib 
                """
                plt.imshow(preprocessed_img, cmap='gray')
                plt.title(f'Preprocessed Image - Page {page_number + 1}, Part {rect_idx + 1}')
                plt.axis('off')
                plt.show()
                """
                
                #Pag 1
                if page_number == 0:
                    if rect_idx == 0: 
                        Nof, Nserie, Mac, TP, TC = text[0].split(': ')[1].replace('O', '0'), text[1].split(': ')[1], text[3].split(': ')[1], text[2].split(': ')[1], text[4].split(': ')[1] # Setupp Parameters
                        print(Nof, Nserie, Mac, TP, TC)
                        all_text.append(f"{Nof} {Nserie} Machine {Mac} \n\n{Nof} {Nserie} Temp_Pieza {TP} \n\n{Nof} {Nserie} Temp_Cabina {TC}") 
                        
                    if rect_idx == 1: 
                        print(f"{Nof} {Nserie} N11-15-Q-FA-{1} {text[1]} \n\n{Nof} {Nserie} N11-15-Q-FA-{2} {text[2]}")              
                        all_text.append(f"{Nof} {Nserie} N11-15-Q-FA-{1} {text[1]} \n\n{Nof} {Nserie} N11-15-Q-FA-{2} {text[2]}")    #N11-15-Q-FA1|2
                    
                    if rect_idx == 2:
                        for data_number in range(len(text) - 8):
                            print(f"{Nof} {Nserie} N11-15-FA-R{text[data_number].lstrip('#')} {text[data_number + 4]} \n\n{Nof} {Nserie} N11-15-FA-R-{text[data_number].lstrip('#')} -{text[data_number + 8][1:]}")
                            all_text.append(f"{Nof} {Nserie} N11-15-FA-R{text[data_number].lstrip('#')} {text[data_number + 4]} \n\n{Nof} {Nserie} N11-15-FA-R-{text[data_number].lstrip('#')} -{text[data_number + 8][1:]}")    #N11-15-FA-R#|-#
                    
                    if rect_idx == 3:
                        for data_number in range(len(text) - 8):
                            print(f"{Nof} {Nserie} N11-15-FNA-R{text[data_number].lstrip('#')} {text[data_number + 4]} \n\n{Nof} {Nserie} N11-15-FNA-R-{text[data_number].lstrip('#')} -{text[data_number + 8][1:]}")
                            all_text.append(f"{Nof} {Nserie} N11-15-FNA-R{text[data_number].lstrip('#')} {text[data_number + 4]} \n\n{Nof} {Nserie} N11-15-FNA-R-{text[data_number].lstrip('#')} -{text[data_number + 8][1:]}")    #N11-15-FNA-R#|-#
                    
                    if rect_idx ==4: 
                        print(f"{Nof} {Nserie} N11-15-Q-FNA-{1} {text[1]} \n\n{Nof} {Nserie} N11-15-Q-FNA-{2} {text[2]}")              
                        all_text.append(f"{Nof} {Nserie} N11-15-Q-FNA-{1} {text[1]} \n\n{Nof} {Nserie} N11-15-Q-FNA-{2} {text[2]}")    #N11-15-Q-FNA1|2
                        
                #Pag 2
                if page_number == 1:                                                 #Setup parameters
                    if rect_idx == 0:
                        print(f"{Nof} {Nserie} N11-16-Q-FA {text[1]}")              
                        all_text.append(f"{Nof} {Nserie} N11-16-Q-FA {text[1]}")    #N11-16-Q-FA
                    
                    if rect_idx == 1:
                        for data_number in range(len(text) - 4):
                            print(f"{Nof} {Nserie} N11-16-FA-R{text[data_number].lstrip('#')} {text[data_number + 4]}")
                            all_text.append(f"{Nof} {Nserie} N11-16-FA-R{text[data_number].lstrip('#')} {text[data_number + 4]}")    #N11-15-FA-R#|-#
                    
                    if rect_idx == 2:
                        for data_number in range(len(text) - 4):
                            print(f"{Nof} {Nserie} N11-16-FNA-R{text[data_number].lstrip('#')} {text[data_number + 4]}")
                            all_text.append(f"{Nof} {Nserie} N11-16-FNA-R{text[data_number].lstrip('#')} {text[data_number + 4]}")    #N11-15-FNA-R#|-#
                    
                    if rect_idx ==3: 
                        print(f"{Nof} {Nserie} N11-16-Q-FA {text[1]}")              
                        all_text.append(f"{Nof} {Nserie} N11-16-Q-FNA {text[1]}")    #N11-16-Q-FNA
                        
                #Pag 4
                if page_number == 3:                                                 #Setup parameters
                    if rect_idx == 0:
                        print(f"{Nof} {Nserie} D123 {text[0].split('/')[0]}")              
                        all_text.append(f"{Nof} {Nserie} D123 {text[0].split('/')[0]}")     #D123
                    
                    elif rect_idx == 1:
                        print(f"{Nof} {Nserie} N11-14-FA {text[0]}")              
                        all_text.append(f"{Nof} {Nserie} N11-14-FA {text[0]}")   #N11-14-FA
                    
                    elif rect_idx == 2:
                        print(f"{Nof} {Nserie} N11-14-FNA {text[0]}")              
                        all_text.append(f"{Nof} {Nserie} N11-14-FNA {text[0]}")   #N11-14-FNA 
                    
                    elif rect_idx == 3: 
                        print(f"{Nof} {Nserie} N11-13-Q-FA {text[0]}")              
                        all_text.append(f"{Nof} {Nserie} N11-13-Q-FA {text[0]}")   #N11-13-Q-FA 
                    
                    elif rect_idx == 4: 
                        print(f"{Nof} {Nserie} N11-13-FA {text[0]}")              
                        all_text.append(f"{Nof} {Nserie} N11-13-FA {text[0]}")   #N11-13-FA 
                        
                    elif rect_idx == 5: 
                        print(f"{Nof} {Nserie} N11-13-Q-FNA {text[0]}")              
                        all_text.append(f"{Nof} {Nserie} N11-13-Q-FNA {text[0]}")   #N11-13-Q-FNA 
                    
                    elif rect_idx == 6: 
                        print(f"{Nof} {Nserie} N11-13-FNA {text[0]}")              
                        all_text.append(f"{Nof} {Nserie} N11-13-FNA {text[0]}")   #N11-13-FNA
                        
                    elif rect_idx == 7: 
                        print(f"{Nof} {Nserie} N07-123 {text[0]}")              
                        all_text.append(f"{Nof} {Nserie} N07-123 {text[0]}")   #N07-123
                
                # Display the preprocessed image using matplotlib 
                """
                plt.imshow(preprocessed_img, cmap='gray')
                plt.title(f'Preprocessed Image - Page {page_number + 1}, Part {rect_idx + 1}')
                plt.axis('off')
                plt.show()
                """

    # Case 2: 3 Pages-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    elif len(pdf_document) == 3:
        for page_number in range(len(pdf_document)):
            # Render page to an image with higher resolution
            page = pdf_document[page_number]
            zoom = 4.0  # Increase this value for higher resolution (e.g., 2.0 = 200% zoom)
            adjust = 4
            matrix = fitz.Matrix(zoom*adjust, zoom*adjust)  # Apply zoom to both x and y axes
            pix = page.get_pixmap(matrix=matrix)  # Render the page with the specified matrix

            # Convert pixmap to numpy array for OpenCV processing
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)

            # Display the preprocessed image using matplotlib 
            """
            plt.imshow(img, cmap='gray')
            plt.title(f'Preprocessed Image - Page {page_number + 1}, Rect {page_number + 1}')
            plt.axis('off')
            plt.show()
            """
            # Define the list of rectangles for the current page
            rectangles = []
            if page_number == 0:
                # Add multiple rectangles for page 1
                rectangles.append((int(300 * adjust), int(270 * adjust), int(7060), int(1451)))  # init
                rectangles.append((int(1995), int(6873), int(2465), int(7414)))  # QFA
                rectangles.append((int(3415), int(6875), int(5300), int(7414)))  # FA
                rectangles.append((int(5767), int(6873), int(7658), int(7414)))  # FNA
                rectangles.append((int(8598), int(6873), int(9067), int(7414)))  # QFNA
                rectangles.append((int(1999), int(12293), int(2467), int(12654)))  # QFA 2
                rectangles.append((int(3412), int(12296), int(5296), int(12654)))  # FA 2
                rectangles.append((int(5768), int(12296), int(7652), int(12654)))  # FNA 2
                rectangles.append((int(8595), int(12293), int(9066), int(12654)))  # QFNA 2
                
            elif page_number == 2:
                rectangles.append((int(720 * adjust), int(545 * adjust), int(940 * adjust), int(590 * adjust)))  # Exz
                rectangles.append((int(1600 * adjust), int(1100 * adjust), int(1820 * adjust), int(1150 * adjust)))  # Fu1
                rectangles.append((int(1600 * adjust), int(1665 * adjust), int(1820 * adjust), int(1710 * adjust)))  # FU2
                rectangles.append((int(1160 * adjust), int(2170 * adjust), int(1380 * adjust), int(2230 * adjust)))  # FP1I
                rectangles.append((int(1600 * adjust), int(2170 * adjust), int(1820 * adjust), int(2230 * adjust)))  # FP1D
                rectangles.append((int(1160 * adjust), int(2690 * adjust), int(1380 * adjust), int(2740 * adjust)))  # FP2I
                rectangles.append((int(1600 * adjust), int(2690 * adjust), int(1820 * adjust), int(2740 * adjust)))  # FP2D
                rectangles.append((int(1600 * adjust), int(3200 * adjust), int(1820 * adjust), int(3250 * adjust)))  # FR

             
            # Process each rectangle
            for rect_idx, (x1, y1, x2, y2) in enumerate(rectangles):
                # Crop the image using the defined coordinates
                cropped_img = img[y1:y2, x1:x2]

                # Convert the cropped image to grayscale
                gray_cropped_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)

                # Preprocess the image (optional)
                preprocessed_img = gray_cropped_img
                
                # Save the preprocessed image
                cropped_image_path = os.path.join(output_dir, f'preprocessed_page_{page_number + 1}_rect_{rect_idx + 1}.jpg')
                cv2.imwrite(cropped_image_path, preprocessed_img)

                # Extract text from cropped image
                text = reader.readtext(cropped_image_path, detail=0)
                print(text)
                
                # Display the preprocessed image using matplotlib 
                """
                plt.imshow(preprocessed_img, cmap='gray')
                plt.title(f'Preprocessed Image - Page {page_number + 1}, Part {rect_idx + 1}')
                plt.axis('off')
                plt.show()
                """
                #Pag 1
                if page_number == 0:
                    if rect_idx == 0: 
                        Nof, Nserie, Mac, TP, TC = text[0].split(': ')[1].replace('O', '0'), text[1].split(': ')[1], text[3].split(': ')[1], text[2].split(': ')[1], text[4].split(': ')[1] # Setupp Parameters
                        print(Nof, Nserie, Mac, TP, TC)
                        all_text.append(f"{Nof} {Nserie} Machine {Mac} \n\n{Nof} {Nserie} Temp_Pieza {TP} \n\n{Nof} {Nserie} Temp_Cabina {TC}") 
                        
                    if rect_idx == 1: 
                        print(f"{Nof} {Nserie} N11-15-Q-FA-{1} {text[1]} \n\n{Nof} {Nserie} N11-15-Q-FA-{2} {text[2]}")              
                        all_text.append(f"{Nof} {Nserie} N11-15-Q-FA-{1} {text[1]} \n\n{Nof} {Nserie} N11-15-Q-FA-{2} {text[2]}")    #N11-15-Q-FA1|2
                    
                    if rect_idx == 2:
                        for data_number in range(len(text) - 8):
                            print(f"{Nof} {Nserie} N11-15-FA-R{text[data_number].lstrip('#')} {text[data_number + 4]} \n\n{Nof} {Nserie} N11-15-FA-R-{text[data_number].lstrip('#')} -{text[data_number + 8][1:]}")
                            all_text.append(f"{Nof} {Nserie} N11-15-FA-R{text[data_number].lstrip('#')} {text[data_number + 4]} \n\n{Nof} {Nserie} N11-15-FA-R-{text[data_number].lstrip('#')} -{text[data_number + 8][1:]}")    #N11-15-FA-R#|-#
                    
                    if rect_idx == 3:
                        for data_number in range(len(text) - 8):
                            print(f"{Nof} {Nserie} N11-15-FNA-R{text[data_number].lstrip('#')} {text[data_number + 4]} \n\n{Nof} {Nserie} N11-15-FNA-R-{text[data_number].lstrip('#')} -{text[data_number + 8][1:]}")
                            all_text.append(f"{Nof} {Nserie} N11-15-FNA-R{text[data_number].lstrip('#')} {text[data_number + 4]} \n\n{Nof} {Nserie} N11-15-FNA-R-{text[data_number].lstrip('#')} -{text[data_number + 8][1:]}")    #N11-15-FNA-R#|-#
                    
                    if rect_idx ==4: 
                        print(f"{Nof} {Nserie} N11-15-Q-FNA-{1} {text[1]} \n\n{Nof} {Nserie} N11-15-Q-FNA-{2} {text[2]}")              
                        all_text.append(f"{Nof} {Nserie} N11-15-Q-FNA-{1} {text[1]} \n\n{Nof} {Nserie} N11-15-Q-FNA-{2} {text[2]}")    #N11-15-Q-FNA1|2
                    
                    if rect_idx == 5:
                        print(f"{Nof} {Nserie} N11-16-Q-FA {text[1]}")              
                        all_text.append(f"{Nof} {Nserie} N11-16-Q-FA {text[1]}")    #N11-16-Q-FA
                    
                    if rect_idx == 6:
                        for data_number in range(len(text) - 4):
                            print(f"{Nof} {Nserie} N11-16-FA-R{text[data_number].lstrip('#')} {text[data_number + 4]}")
                            all_text.append(f"{Nof} {Nserie} N11-16-FA-R{text[data_number].lstrip('#')} {text[data_number + 4]}")    #N11-15-FA-R#|-#
                    
                    if rect_idx == 7:
                        for data_number in range(len(text) - 4):
                            print(f"{Nof} {Nserie} N11-16-FNA-R{text[data_number].lstrip('#')} {text[data_number + 4]}")
                            all_text.append(f"{Nof} {Nserie} N11-16-FNA-R{text[data_number].lstrip('#')} {text[data_number + 4]}")    #N11-15-FNA-R#|-#
                    
                    if rect_idx == 8: 
                        print(f"{Nof} {Nserie} N11-16-Q-FA {text[1]}")              
                        all_text.append(f"{Nof} {Nserie} N11-16-Q-FNA {text[1]}")    #N11-16-Q-FNA
                    
                if page_number == 2:                                                 #Setup parameters
                    if rect_idx == 0:
                        print(f"{Nof} {Nserie} D123 {text[0].split('/')[0]}")              
                        all_text.append(f"{Nof} {Nserie} D123 {text[0].split('/')[0]}")     #D123
                    
                    elif rect_idx == 1:
                        print(f"{Nof} {Nserie} N11-14-FA {text[0]}")              
                        all_text.append(f"{Nof} {Nserie} N11-14-FA {text[0]}")   #N11-14-FA
                    
                    elif rect_idx == 2:
                        print(f"{Nof} {Nserie} N11-14-FNA {text[0]}")              
                        all_text.append(f"{Nof} {Nserie} N11-14-FNA {text[0]}")   #N11-14-FNA 
                    
                    elif rect_idx == 3: 
                        print(f"{Nof} {Nserie} N11-13-Q-FA {text[0]}")              
                        all_text.append(f"{Nof} {Nserie} N11-13-Q-FA {text[0]}")   #N11-13-Q-FA 
                    
                    elif rect_idx == 4: 
                        print(f"{Nof} {Nserie} N11-13-FA {text[0]}")              
                        all_text.append(f"{Nof} {Nserie} N11-13-FA {text[0]}")   #N11-13-FA 
                        
                    elif rect_idx == 5: 
                        print(f"{Nof} {Nserie} N11-13-Q-FNA {text[0]}")              
                        all_text.append(f"{Nof} {Nserie} N11-13-Q-FNA {text[0]}")   #N11-13-Q-FNA 
                    
                    elif rect_idx == 6: 
                        print(f"{Nof} {Nserie} N11-13-FNA {text[0]}")              
                        all_text.append(f"{Nof} {Nserie} N11-13-FNA {text[0]}")   #N11-13-FNA
                        
                    elif rect_idx == 7: 
                        print(f"{Nof} {Nserie} N07-123 {text[0]}")              
                        all_text.append(f"{Nof} {Nserie} N07-123 {text[0]}")   #N07-123
                        
                
    # Case 3: 26 Pages----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    elif len(pdf_document) > 4:
        for page_number in range(len(pdf_document)):
            # Render page to an image with higher resolution
            page = pdf_document[page_number]
            zoom = 4.0  # Increase this value for higher resolution (e.g., 2.0 = 200% zoom)
            adjust = 4
            matrix = fitz.Matrix(zoom*adjust, zoom*adjust)  # Apply zoom to both x and y axes
            pix = page.get_pixmap(matrix=matrix)  # Render the page with the specified matrix

            # Convert pixmap to numpy array for OpenCV processing
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)

            # Display the preprocessed image using matplotlib 
            """
            plt.imshow(img, cmap='gray')
            plt.title(f'Preprocessed Image - Page {page_number + 1}, Rect {page_number + 1}')
            plt.axis('off')
            plt.show()
            """
        
            # Define the list of rectangles for the current page            
            rectangles = []
            if page_number == 0:
                # Add multiple rectangles for page 1
                rectangles.append((int(300 * adjust), int(270 * adjust), int(7060), int(1451)))  # INIT NSERIE NOF MACHINE
                rectangles.append((int(2820), int(12290), int(5330), int(12834)))  # #FA
                rectangles.append((int(5748), int(12285), int(8234), int(12834)))  # #FNA
                
            elif page_number >= 1 and page_number < 11:
                rectangles.append((int(2820), int(12290), int(5330), int(12834)))  # #FA
                rectangles.append((int(5748), int(12285), int(8234), int(12834)))  # #FNA
            
            elif page_number == 11: 
                rectangles.append((int(2000), int(12295), int(2450), int(12830)))  # Q FA
                rectangles.append((int(8600), int(12300), int(9068), int(12830)))  # Q FNA
                rectangles.append((int(3430), int(12300), int(5295), int(12830)))  # #FA
                rectangles.append((int(5775), int(12300), int(7650), int(12830)))  # #FNA
                    
            elif page_number >= 12 and page_number < 23:
                rectangles.append((int(2820), int(12290), int(5330), int(12834)))  # #FA
                rectangles.append((int(5748), int(12285), int(8234), int(12834)))  # #FNA
            
            elif page_number == 23:
                rectangles.append((int(2000), int(12295), int(2450), int(12830)))  # Q FA
                rectangles.append((int(8600), int(12300), int(9068), int(12830)))  # Q FNA
                rectangles.append((int(3430), int(12300), int(5295), int(12830)))  # #FA
                rectangles.append((int(5775), int(12300), int(7650), int(12830)))  # #FNA
                
            elif page_number == 25:
                rectangles.append((int(720 * adjust), int(545 * adjust), int(940 * adjust), int(590 * adjust)))  # Exz
                rectangles.append((int(1600 * adjust), int(1100 * adjust), int(1820 * adjust), int(1150 * adjust)))  # Fu1
                rectangles.append((int(1600 * adjust), int(1665 * adjust), int(1820 * adjust), int(1710 * adjust)))  # FU2
                rectangles.append((int(1160 * adjust), int(2170 * adjust), int(1380 * adjust), int(2230 * adjust)))  # FP1I
                rectangles.append((int(1600 * adjust), int(2170 * adjust), int(1820 * adjust), int(2230 * adjust)))  # FP1D
                rectangles.append((int(1160 * adjust), int(2690 * adjust), int(1380 * adjust), int(2740 * adjust)))  # FP2I
                rectangles.append((int(1600 * adjust), int(2690 * adjust), int(1820 * adjust), int(2740 * adjust)))  # FP2D
                rectangles.append((int(1600 * adjust), int(3200 * adjust), int(1820 * adjust), int(3250 * adjust)))  # FR
                
            # Process each rectangle
            for rect_idx, (x1, y1, x2, y2) in enumerate(rectangles):
                # Crop the image using the defined coordinates
                cropped_img = img[y1:y2, x1:x2]

                # Convert the cropped image to grayscale
                gray_cropped_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)

                # Preprocess the image (optional)
                preprocessed_img = gray_cropped_img
                
                # Save the preprocessed image
                cropped_image_path = os.path.join(output_dir, f'preprocessed_page_{page_number + 1}_rect_{rect_idx + 1}.jpg')
                cv2.imwrite(cropped_image_path, preprocessed_img)

                # Extract text from cropped image
                text = reader.readtext(cropped_image_path, detail=0)
                print(f"{text}")
                
                # Display the preprocessed image using matplotlib (optional)
                """
                plt.imshow(preprocessed_img, cmap='gray')
                plt.title(f'Preprocessed Image - Page {page_number + 1}, Part {rect_idx + 1}')
                plt.axis('off')
                plt.show()
                """
                
                #Pag 1
                if page_number == 0:
                    if rect_idx == 0: 
                        Nof, Nserie, Mac, TP, TC = text[0].split(': ')[1].replace('O', '0'), text[1].split(': ')[1], text[3].split(': ')[1], text[2].split(': ')[1], text[4].split(': ')[1] # Setupp Parameters
                        print(Nof, Nserie, Mac, TP, TC)
                        all_text.append(f"{Nof} {Nserie} Machine {Mac} \n\n{Nof} {Nserie} Temp_Pieza {TP} \n\n{Nof} {Nserie} Temp_Cabina {TC}") 
                                          
                    elif rect_idx == 1:
                        for data_number in range(len(text) - 12):
                            print(f"{Nof} {Nserie} N11-15-FA-R{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} {text[data_number + 6]} \n\n{Nof} {Nserie} N11-15-FA-R-{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} -{text[data_number + 12][1:]}")
                            all_text.append(f"{Nof} {Nserie} N11-15-FA-R{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} {text[data_number + 6]} \n\n{Nof} {Nserie} N11-15-FA-R-{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} -{text[data_number + 12][1:]}")    #N11-15-FA-R#|-#
                    
                    if rect_idx == 2:
                        for data_number in range(len(text) - 12):
                            print(f"{Nof} {Nserie} N11-15-FNA-R{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} {text[data_number + 6]} \n\n{Nof} {Nserie} N11-15-FNA-R-{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} -{text[data_number + 12][1:]}")
                            all_text.append(f"{Nof} {Nserie} N11-15-FNA-R{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} {text[data_number + 6]} \n\n{Nof} {Nserie} N11-15-FNA-R-{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} -{text[data_number + 12][1:]}")    #N11-15-FNA-R#|-#
                    
                #Pag 2-11
                elif page_number >= 1 and page_number < 11:                                                 #Setup parameters
                    if rect_idx == 0:
                        for data_number in range(len(text) - 12):
                            print(f"{Nof} {Nserie} N11-15-FA-R{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} {text[data_number + 6]} \n\n{Nof} {Nserie} N11-15-FA-R-{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} -{text[data_number + 12][1:]}")
                            all_text.append(f"{Nof} {Nserie} N11-15-FA-R{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} {text[data_number + 6]} \n\n{Nof} {Nserie} N11-15-FA-R-{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} -{text[data_number + 12][1:]}")    #N11-15-FA-R#|-#
                    
                    elif rect_idx == 1:
                        for data_number in range(len(text) - 12):
                            print(f"{Nof} {Nserie} N11-15-FNA-R{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} {text[data_number + 6]} \n\n{Nof} {Nserie} N11-15-FNA-R-{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} -{text[data_number + 12][1:]}")
                            all_text.append(f"{Nof} {Nserie} N11-15-FNA-R{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} {text[data_number + 6]} \n\n{Nof} {Nserie} N11-15-FNA-R-{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} -{text[data_number + 12][1:]}")    #N11-15-FNA-R#|-#
                
                #Page 12
                elif page_number == 11:
                    if rect_idx == 0: 
                        print(f"{Nof} {Nserie} N11-15-{text[0]}-FA-{1} {text[1]} \n\n{Nof} {Nserie} N11-15-Q-FA-{2} {text[2]}")              
                        all_text.append(f"{Nof} {Nserie} N11-15-{text[0]}-FA-{1} {text[1]} \n\n{Nof} {Nserie} N11-15-Q-FA-{2} {text[2]}")    #N11-15-Q-FA1|2
                    
                    elif rect_idx == 1: 
                        print(f"{Nof} {Nserie} N11-15-{text[0]}-FNA-{1} {text[1]} \n\n{Nof} {Nserie} N11-15-Q-FNA-{2} {text[2]}")              
                        all_text.append(f"{Nof} {Nserie} N11-15-{text[0]}-FNA-{1} {text[1]} \n\n{Nof} {Nserie} N11-15-Q-FNA-{2} {text[2]}")    #N11-15-Q-FNA1|2
                        
                    elif rect_idx == 2:
                        for data_number in range(len(text) - 8):
                            print(f"{Nof} {Nserie} N11-15-FA-R{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} {text[data_number + 4]} \n\n{Nof} {Nserie} N11-15-FA-R-{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} -{text[data_number + 8][1:]}")
                            all_text.append(f"{Nof} {Nserie} N11-15-FA-R{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} {text[data_number + 4]} \n\n{Nof} {Nserie} N11-15-FA-R-{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} -{text[data_number + 8][1:]}")    #N11-15-FA-R#|-#
                    
                    elif rect_idx == 3:
                        for data_number in range(len(text) - 8):
                            print(f"{Nof} {Nserie} N11-15-FNA-R{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} {text[data_number + 4]} \n\n{Nof} {Nserie} N11-15-FNA-R-{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} -{text[data_number + 8][1:]}")
                            all_text.append(f"{Nof} {Nserie} N11-15-FNA-R{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} {text[data_number + 4]} \n\n{Nof} {Nserie} N11-15-FNA-R-{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} -{text[data_number + 8][1:]}")    #N11-15-FNA-R#|-#
                
                #Pag 13-23
                elif page_number >= 12 and page_number < 23:                                                #Setup parameters
                    if rect_idx == 0:
                        for data_number in range(len(text) - 6):
                            print(f"{Nof} {Nserie} N11-16-FA-R{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} {text[data_number + 6]}")
                            all_text.append(f"{Nof} {Nserie} N11-16-FA-R{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} {text[data_number + 6]}")    #N11-16-FA-R#|-#
                    
                    elif rect_idx == 1:
                        for data_number in range(len(text) - 6):
                            print(f"{Nof} {Nserie} N11-16-FNA-R{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} {text[data_number + 6]}")
                            all_text.append(f"{Nof} {Nserie} N11-16-FNA-R{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} {text[data_number + 6]}")    #N11-16-FNA-R#|-#
                
                #Page 24
                elif page_number == 23:
                    if rect_idx == 0: 
                        print(f"{Nof} {Nserie} N11-16-Q-FA-{1} {text[1]}")              
                        all_text.append(f"{Nof} {Nserie} N11-16-Q-FA-{1} {text[1]}")    #N11-16-Q-FA1|2
                    
                    elif rect_idx == 1: 
                        print(f"{Nof} {Nserie} N11-16-Q-FNA-{1} {text[1]}")              
                        all_text.append(f"{Nof} {Nserie} N11-16-Q-FNA-{1} {text[1]}")    #N11-16-Q-FNA1|2
                        
                    elif rect_idx == 2:
                        for data_number in range(len(text) - 4):
                            print(f"{Nof} {Nserie} N11-16-FA-R{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} {text[data_number + 4]}")
                            all_text.append(f"{Nof} {Nserie} N11-16-FA-R{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} {text[data_number + 4]}")    #N11-16-FA-R#
                    
                    elif rect_idx == 3:
                        for data_number in range(len(text) - 4):
                            print(f"{Nof} {Nserie} N11-16-FNA-R{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} {text[data_number + 4]}")
                            all_text.append(f"{Nof} {Nserie} N11-16-FNA-R{text[data_number].lstrip('#').replace('O', '0').replace('o', '0')} {text[data_number + 4]}")    #N11-16-FNA-R#
                
                #Pag 26 (25 da igual)            
                if page_number == 25:                                                 #Setup parameters
                    if rect_idx == 0:
                        print(f"{Nof} {Nserie} D123 {text[0].split('/')[0]}")              
                        all_text.append(f"{Nof} {Nserie} D123 {text[0].split('/')[0]}")     #D123
                    
                    elif rect_idx == 1:
                        print(f"{Nof} {Nserie} N11-14-FA {text[0]}")              
                        all_text.append(f"{Nof} {Nserie} N11-14-FA {text[0]}")   #N11-14-FA
                    
                    elif rect_idx == 2:
                        print(f"{Nof} {Nserie} N11-14-FNA {text[0]}")              
                        all_text.append(f"{Nof} {Nserie} N11-14-FNA {text[0]}")   #N11-14-FNA 
                    
                    elif rect_idx == 3: 
                        print(f"{Nof} {Nserie} N11-13-Q-FA {text[0]}")              
                        all_text.append(f"{Nof} {Nserie} N11-13-Q-FA {text[0]}")   #N11-13-Q-FA 
                    
                    elif rect_idx == 4: 
                        print(f"{Nof} {Nserie} N11-13-FA {text[0]}")              
                        all_text.append(f"{Nof} {Nserie} N11-13-FA {text[0]}")   #N11-13-FA 
                        
                    elif rect_idx == 5: 
                        print(f"{Nof} {Nserie} N11-13-Q-FNA {text[0]}")              
                        all_text.append(f"{Nof} {Nserie} N11-13-Q-FNA {text[0]}")   #N11-13-Q-FNA 
                    
                    elif rect_idx == 6: 
                        print(f"{Nof} {Nserie} N11-13-FNA {text[0]}")              
                        all_text.append(f"{Nof} {Nserie} N11-13-FNA {text[0]}")   #N11-13-FNA
                        
                    elif rect_idx == 7: 
                        print(f"{Nof} {Nserie} N07-123 {text[0]}")              
                        all_text.append(f"{Nof} {Nserie} N07-123 {text[0]}")   #N07-123
                
    pdf_document.close()
    return "\n\n".join(all_text)

#MAIN---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    #pdf_file = r"C:\Users\sm10244\Downloads\DFB;OP1700V002.1;Fbeta_alfa_20250322 183414_3444_DFB0004586_HB155308-M.pdf"  #Caso 1
    #pdf_file = r"C:\Users\sm10244\Downloads\DFB;OP1700V002.1;Fbeta_alfa_20240125 020828_2353_DFB0003748_PF294445-A.pdf"   #Caso 2
    #pdf_file = r"C:\Users\sm10244\Downloads\DFB;OP1700V002.1;Fbeta_alfa_20250325 145120_3454_DFB0004591_HB155079-5.pdf"  #Caso 3
    #pdf_file = r"C:\Users\sm10244\Downloads\DFB;OP1700V002.1;Fbeta_alfa_20250405 052856_3482_DFB0004619_HB155752-6.pdf" #Caso 4 (1 dificil)
    
    """
    # Create a Tkinter root window (hidden)
    root = Tk()
    root.withdraw()

    # Open a file dialog to select a PDF file
    pdf_file = filedialog.askopenfilename(
        title="Select a PDF file",
        filetypes=[("PDF files", "*.pdf")]
    )
    """
    
    if len(sys.argv) > 1:
        pdf_file = sys.argv[1]  # Obtener la ruta del archivo PDF desde los argumentos
    else:
        # Si no se pasa un argumento, abrir un cuadro de diálogo para seleccionar el archivo
        root = Tk()
        root.withdraw()
        pdf_file = filedialog.askopenfilename(
            title="Select a PDF file",
            filetypes=[("PDF files", "*.pdf")]
        )

    # Check if a file was selected
    if not pdf_file:
        print("No file selected. Exiting...")
        exit()
    
    output_directory = "output_images"  # Directory to save images
    extracted_text = pdf_to_text(pdf_file, output_directory)

    # Save extracted text to a CSV file
    csv_file_path = f"{pdf_file}_extracted_text.csv"
    with open(csv_file_path, mode="w", encoding="utf-8", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Nof", "Nserie", "Cota", "Valor"])  # Header row
        for line in extracted_text.split("\n\n"):
            parts = line.split()
            if len(parts) >= 4:
                csv_writer.writerow([parts[0], parts[1], parts[2], parts[3]])

    print(f"Extracted text saved to {csv_file_path}")

    print(extracted_text)
    print("Text extraction complete. Check 'extracted_text.txt' for results.")