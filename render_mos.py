#!/usr/bin/env python3
from jinja2 import FileSystemLoader, Environment
from utils import QuestionGenerator_MOS as QuestionGenerator
import random

def make_question_html(q, model):
    options = [(5,"Very Good"),(4,"Good"),(3,"Fair"),(2,"Bad"),(1,"Very Bad")]
    opts_html = ""
    for v, label in options:
        opts_html += f"""
                <div class="form-check">
                    <input class="form-check-input" type="radio" name="{q['name']}" value="{v}" required>
                    <label class="form-check-label">{v} — {label}</label>
                </div>"""
    return f"""
        <div class="question" data-question-id="{q['id']}" data-model="{model}">
            <div class="card-header">{q['title']}</div>
            <div class="card-body">
                <audio controls src="{q['audio_path']}" style="width:100%;margin-bottom:10px;">
                    Your browser does not support the audio element.
                </audio>
                {opts_html}
            </div>
        </div>"""

def main():
    # load all questions
    model1 = QuestionGenerator("filelist/audio_order.csv").questions
    model2 = QuestionGenerator("filelist/model2.csv").questions

    # pick 10 random from each
    selected1 = random.sample(model1, 10)
    selected2 = random.sample(model2, 10)

    # renumber
    for i, q in enumerate(selected1, start=1):
        q["id"] = i
        q["title"] = f"Question {i}"
        q["name"] = f"m1_q{i}"

    for i, q in enumerate(selected2, start=1):
        q["id"] = i
        q["title"] = f"Question {i}"
        q["name"] = f"m2_q{i}"

    # build questions html
    page1_questions = "".join(make_question_html(q, 1) for q in selected1)
    page2_questions = "".join(make_question_html(q, 2) for q in selected2)

    html = """<!doctype html>
<html>
<head>
    <title>MOS Experiment</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.1/css/bootstrap.min.css"
        integrity="sha384-VCmXjywReHh4PwowAiWNagnWcLhlEJLA5buUprzK8rxFgeH0kww/aWY76TfkUoSX" crossorigin="anonymous">
    <style>
        .page { display: none; }
        .page.active { display: block; }
        .progress-bar-container { background:#e9ecef; border-radius:4px; height:8px; margin-bottom:20px; }
        .progress-bar-fill { background:#17a2b8; height:8px; border-radius:4px; transition:width 0.3s; }
        .question { margin-bottom:20px; border:1px solid #dee2e6; border-radius:4px; }
        .card-header { background:#f8f9fa; padding:10px 15px; font-weight:bold; }
        .card-body { padding:15px; }
    </style>
</head>
<body>

<!-- PAGE 1 -->
<div class="page active" id="page1">
    <div class="jumbotron jumbotron-fluid">
        <div class="container">
            <h1 class="display-4">MOS Experiment</h1>
            <p class="lead">Synthetic Speech Quality Evaluation — Part 1 of 2</p>
            <hr class="my-4">
            <p>Welcome! You will evaluate <b>two sets</b> of audio samples. Please rate each audio from 1 to 5:</p>
            <ul>
                <li><b>5 (Very Good)</b>: Exceptionally clear, natural, and pleasant.</li>
                <li><b>4 (Good)</b>: Clear and pleasant with only minor issues.</li>
                <li><b>3 (Fair)</b>: Somewhat clear but with some issues.</li>
                <li><b>2 (Bad)</b>: Noticeable issues, uncomfortable to listen to.</li>
                <li><b>1 (Very Bad)</b>: Highly distorted, difficult to understand.</li>
            </ul>
            <p>Please use headphones for the best experience.</p>
        </div>
    </div>
    <div class="container">
        <div class="progress-bar-container">
            <div class="progress-bar-fill" style="width:50%"></div>
        </div>
        <p class="text-muted">Part 1 of 2</p>
        <div class="form-group">
            <label>Gender:</label>
            <select class="form-control" id="gender" required>
                <option value="" disabled selected>Select your gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
            </select>
            <small class="form-text text-muted">Required*</small>
        </div>
        PAGE1_QUESTIONS
        <br>
        <button class="btn btn-info btn-lg" onclick="goToPage2()">Next → Part 2</button>
        <p class="text-muted mt-2"><small>Please answer all questions and select your gender before continuing.</small></p>
    </div>
</div>

<!-- PAGE 2 -->
<div class="page" id="page2">
    <div class="jumbotron jumbotron-fluid">
        <div class="container">
            <h1 class="display-4">MOS Experiment</h1>
            <p class="lead">Synthetic Speech Quality Evaluation — Part 2 of 2</p>
            <hr class="my-4">
            <p>You are now on the second and final set. Please rate each audio from 1 to 5 using the same scale.</p>
        </div>
    </div>
    <div class="container">
        <div class="progress-bar-container">
            <div class="progress-bar-fill" style="width:100%"></div>
        </div>
        <p class="text-muted">Part 2 of 2</p>
        PAGE2_QUESTIONS
        <br>
        <button class="btn btn-info btn-lg" onclick="submitAll()">Submit All Results</button>
        <p class="text-muted mt-2"><small>Please answer all questions before submitting.</small></p>
    </div>
</div>

<div class="container" style="padding-top:60px;">
    <p class="text-center text-muted">&copy; MOS Evaluation</p>
</div>

<script>
function goToPage2() {
    const gender = document.getElementById('gender').value;
    if (!gender) { alert('Please select your gender.'); return; }
    const questions = document.querySelectorAll('#page1 .question');
    for (let q of questions) {
        const checked = q.querySelector('input[type=radio]:checked');
        if (!checked) { alert('Please answer all questions in Part 1 before continuing.'); return; }
    }
    document.getElementById('page1').classList.remove('active');
    document.getElementById('page2').classList.add('active');
    window.scrollTo(0, 0);
}

function submitAll() {
    const questions = document.querySelectorAll('#page2 .question');
    for (let q of questions) {
        const checked = q.querySelector('input[type=radio]:checked');
        if (!checked) { alert('Please answer all questions in Part 2 before submitting.'); return; }
    }
    const gender = document.getElementById('gender').value;
    let text = 'Gender: ' + gender + '\\n\\n';
    text += '--- Model 1 ---\\n';
    document.querySelectorAll('#page1 .question').forEach(q => {
        const id = q.getAttribute('data-question-id');
        const audio = q.querySelector('audio').src.split('/').pop();
        const score = q.querySelector('input[type=radio]:checked').value;
        text += 'Question ' + id + ' (' + audio + '): ' + score + '\\n';
    });
    text += '\\n--- Model 2 ---\\n';
    document.querySelectorAll('#page2 .question').forEach(q => {
        const id = q.getAttribute('data-question-id');
        const audio = q.querySelector('audio').src.split('/').pop();
        const score = q.querySelector('input[type=radio]:checked').value;
        text += 'Question ' + id + ' (' + audio + '): ' + score + '\\n';
    });
    const blob = new Blob([text], { type: 'text/plain' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'mos_results.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    alert('Thank you! Please send the downloaded file to the researcher.');
}
</script>
</body>
</html>"""

    html = html.replace("PAGE1_QUESTIONS", page1_questions)
    html = html.replace("PAGE2_QUESTIONS", page2_questions)

    with open("rendered_mos.html", "w") as f:
        f.write(html)
        print("Done!")

if __name__ == "__main__":
    main()
