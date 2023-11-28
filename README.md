# Image Encryption Project

## Overview
This GitHub project implements three image encryption algorithms inspired by research papers. The algorithms leverage principles from the Josephus problem, filtering technology, chaotic maps, and row/column switching to achieve efficient and secure visual technology for protecting private images.

## Algorithms Implemented

### 1. Josephus Problem and Filtering Diffusion Encryption
- The encryption algorithm utilizes the Josephus problem for pixel shuffling and filtering technology for diffusion.
- Classical diffusion and confusion structure is followed for enhanced security.
- Simulation results demonstrate uniform distribution in cipher images.
- The algorithm exhibits sensitivity to the secret key, resistance to various security attacks, and outperforms several advanced image encryption algorithms.
- [Read More](https://link.springer.com/article/10.1007/s11071-014-1729-y)

### 2. Josephus Traversing and Mixed Chaotic Map Encryption
- Similar to the first algorithm, this approach combines the Josephus problem and filtering technology.
- Follows classical diffusion and confusion structure for image encryption.
- Simulation results show encryption capabilities for various image types with uniform distribution.
- Security analysis indicates sensitivity to the secret key, resistance to security attacks, and superior performance compared to advanced image encryption algorithms.
- [Read More](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8598711)

### 3. Fast Image Algorithm Based on Rows and Columns Switch
- Proposes a fast image encryption algorithm based on rows and columns switch.
- Shuffling involves rows and columns, with simultaneous encryption of pixels using a key.
- Utilizes a logistic map to generate keys and switched indexes, reducing the iteration count for faster execution.
- Demonstrates significantly faster speed compared to other algorithms based on research data.
- Shows resilience against differential attacks, statistical analysis, known-plaintext, and chosen-plaintext attacks.
- [Read More](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8301018)


## Project Setup and Execution Guide

Follow these steps to set up and run the project:

1. **Clone the GitHub Repository** : git clone https://github.com/SaiShanmukkha/Image-Encryption---JPMCM.git
2. **Navigate to the Project Directory** : cd [name of the folder]. Open Terminal in the Project Folder and Ensure that you're in the correct directory.
3. **Install Required Dependencies**: Make sure you have Python 3.x installed in the system and run "pip install -r requirements.txt"
4. **Configure the Script** : Open main.py in a text editor and Change the input image path to your desired file.
5. **Run the Script** : python main.py
6. **Navigate to the Images folder**: Find the encrypted image "eimage.png" and decrypted image "dimage.png" in ./Images/Output Folder.


## Contributions
Contributions are welcome! Feel free to fork the repository, make improvements, and create pull requests. Please ensure adherence to the project's coding standards and documentation guidelines.

## License
This project is licensed under the [Apache License](LICENSE.md). Feel free to use, modify, and distribute as per the terms of the license.

## Functionalities check
All the functionalities does work in the final version of the application.

## Acknowledgments
- The algorithms implemented in this project are based on the research papers:
  - [Josephus Problem and Filtering Diffusion](https://link.springer.com/article/10.1007/s11071-014-1729-y)
  - [Josephus Traversing and Mixed Chaotic Map](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8598711)
  - [Fast Image Algorithm Based on Rows and Columns Switch](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8301018)

## Contact
For inquiries, issues, or collaboration, please contact the project maintainers:
- Sai Shanmukkha Surapaneni (siv30@txstate.edu)
- Ganesh Gaiy (ane80@txstate.edu)
- Kalyan Chittipeddi(jnw96@txstate.edu)
- Raju Kumar Madala (vks20@txstate.edu)
