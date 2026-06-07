# Intro 
The project is auxlilliary to the BLE Navigator. It serves to translate the SVG file's shapes into a grid compatible with the application's logic.
There are 2 reasons for it's existance.
### 1. The logic is time-consuming
This Python code executes in 3 seconds, yet an identically structured function in the BLE Navigator mobile application is significantly slower.
There is no need to slow down the application.
### 2. The calculation is external to navigation.
Neither the user nor the app have any use for it outside of the initiation phase. Leaving it to an external program not only accelerates testing and debugging, but also
makes it easier to apply to other projects.

# Usage
1. Replace bigmap.svg with the desired file.
2. Run the program.
3. The result is automatically copied to your clipboard, simply paste it in your preferred location.
