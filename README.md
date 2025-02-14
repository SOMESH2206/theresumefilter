# Resume Alignment Program

## Description
This program takes multiple resume files and a list of requirements as input, then processes and analyzes them to determine the best-aligned resume. It helps in filtering and ranking resumes based on the given criteria, making recruitment more efficient.

## Features
- Accepts multiple resume files (PDF, DOCX, TXT, etc.).
- Analyzes resumes based on user-provided job requirements.
- Uses text processing and similarity analysis to rank resumes.
- Outputs the best-matched resume based on the given criteria.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/SOMESH2206/RESUMESORTER.git
   cd RESUMESORTER
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Place all resume files in the `resumes/` folder.
2. Provide job requirements in a text file (`requirements.txt`).
3. Run the program:
   ```bash
   python main.py --resumes ./resumes --requirements requirements.txt
   ```
4. The program will output the best-matched resume and display the ranking.

## Example
```bash
python main.py --resumes ./resumes --requirements job_description.txt
```


## Requirements
- Python 3.x
- Libraries: `nltk`, `flask`, `PyPDF2`, `logging`

## Contributing
Feel free to contribute by submitting issues or pull requests.

## Contact
For queries, contact 24364@iiitu.ac.in or visit [GitHub](https://github.com/SOMESH2206).

