FROM python:3

WORKDIR /usr/src/app

COPY ptt_all_post_v3.requirements ./
RUN pip install --no-cache-dir -r ptt_all_post_v3.requirements

COPY . .
CMD [ "python", "./ptt_all_post_v3.py", "-d", "1", "-o", "./output.txt" ]
