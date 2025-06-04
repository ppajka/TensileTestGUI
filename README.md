# TensileTestGUI

1. Install PyCharm and set Python 3.11 as the interpreter.  

2. Download the GUI Python files.  

3. Create a folder location for the test images.  

4. Create an excel file for the test data.  

5. Install the following modules:  
  a) Customtkinter  
  b) Opencv-python  
  c) Pillow  
  d) Pandas  
  e) Openpyxl  
  f) Pypylon  
  g) Pyserial  

6. Run the GUI.py script.  
  a) Input the test images folder location in the first text box prompt.  
  b) Input the test excel file location in the second text box prompt.  

7. Press the “Configure Cameras” button.  
  a) Adjust the gain and exposure to desirable values for DIC.  
  b) Set the image acquisition rate.  
  c) Close the window.  

8. Press the “Configure Load Frame” button.  
  a) Select the specimen type in the drop down.  
  b) Input width, depth, or diameter values.  
  c) Set the load acquisition rate. 
  d) Select the test type in the drop down.  
  e) Close the window.  

9. Press the “Start Test” button.  
  a) Upon completion, stop the code (occasionally this will need to be pressed twice to ensure the threads are stopped)  

10. Run the GUI.py script again.  
  a) Input the image folder location in the first text box prompt.  
  b) Input the last image file location in the third text box prompt.  

11. Select the “Launch Image Trimming” button.  
  a) Click and drag to create a desired rectangular crop region.  
  b) Select the “Confirm Selection” button.  
  c) Select the “Crop Images” button.  

12. Upload all cropped images to VIC-3D (follow the instructions in DIC section) 

13. Extract the data to a .csv file.  

14. Set focus on the GUI window.  
  a) Input the file location of the extracted .csv  

15. Press the “Output Results” to display values/plots according to user preferences.  

16. Stop the script.  


