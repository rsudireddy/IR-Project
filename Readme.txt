Instruction to run project
1. Open the project folder in Linux/ terminal
2. Navigate to Spiders folder
              cd myproject
              cd spiders 
3. Enter Scrapy crawl my_crawler in linux
4. Next navigate to flask folder and run the python code
               cd ..
               cd flask
               python3 query_processor.python
5. Open another terminal and run make a request to flask server
                  curl -X POST http://localhost:5000/query -H "Content-Type: application/json" -d '{"query": "javascript"}'         


prerequisites:
pip install Scrapy
pip install scikit-learn
pip install flask
pip install request      
pip install beautifulsoup4