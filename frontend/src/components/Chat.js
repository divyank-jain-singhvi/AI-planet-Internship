import React,{useState} from 'react'
import axios from 'axios';
import './Chat.css'
import ai from '../asserts/ai.png'
import group from '../asserts/Group 4.png'


function FormattedText({ text }) {
  // Check if text is defined before processing
  if (!text) {
    return null; // Or any other fallback behavior you prefer
  }

  // Split the text into lines
  const lines = text.split('\n');

  // Map through each line and wrap them in <div> elements
  const formattedLines = lines.map((line, index) => {
    // Check if the line starts with '*'
    if (line.trim().startsWith('*')) {
      // Add a newline character before the line
      return (
        <React.Fragment key={index}>
          <br />
          {line.trim()}
        </React.Fragment>
      );
    } else {
      return (
        <div key={index}>{line.trim()}</div>
      );
    }
  });

  return (
    <div>
      {formattedLines}
    </div>
  );
}


export default function Chat() {

    const[question,setQuestion]=useState("");
    const[outputs,setoutputs]=useState("Terminal");
    const SendQuestion = async () => {
    console.log(question)
    let QuestionBlock = {
        'question':question,
        'answer': 'result',
    };
        await axios({
            method: 'post',
            url: 'http://localhost:8000/',
            data: QuestionBlock,
            headers: {
                'Content-Type': 'application/json'
            }
        }).then((response) => {
            console.log(response.data);
        }).catch((error) => {
            console.error("Error:", error);
        });
        const response=await axios.get('http://localhost:8000/')
        console.log(response.data)
        setoutputs(response.data)
    };
  return (
    <>
        <div className='chat-main'>
            <div className='one-chat-div'>
                <div className='question'><img src={group} alt='' className='bot-image'></img>{outputs[Object.keys(outputs).length-1].question}</div>
                <div className='result'><img src={ai} alt='' className='question-image'></img><FormattedText text={outputs[Object.keys(outputs).length-1].answer}/></div>
            </div>
            <div className='question-input-block'>
                <input className='question-input shadow' placeholder='Send a message...' type="text" onChange={(e)=>setQuestion(e.target.value)} value={question} required></input>
                <button onClick={SendQuestion} className='submit-btn'>→</button>
            </div>

            </div>
  
    </>
  )
}
