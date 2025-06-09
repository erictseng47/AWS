

This is an AWS operations project that includes basic operations for EC2, S3, and SQS.

---

## 📂 Project Structure

```
├── main.py                 # Main script responsible for executing the overall project workflow
├── utils.py                # Encapsulates AWS SDK (boto3) functions, dedicated to interacting with AWS, including logic for S3 upload, SQS send/receive, EC2 launch, etc.
├── config.py               # Responsible for loading the configuration file (.env)
├── CSE546_YenKai_Tseng.txt # Test file to be uploaded to S3
├── .env                    # Personal environment variables
├── requirements.txt        # List of required packages; install them using `pip install -r requirements.txt`
└── README.md               # Documentation (this file)
```

---

## ⚙️ Installation & Execution Steps

### 1️⃣ Install Required Packages
```bash
pip install -r requirements.txt
```

### 2️⃣ Run the Program
```bash
python3 main.py
```