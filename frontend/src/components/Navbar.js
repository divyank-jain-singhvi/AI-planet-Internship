import React,{useState} from 'react'
import AI_Planet_Logo from '../asserts/AI Planet Logo.png'
import axios from 'axios';
import './Navbar.css'

export default function Navbar() {


    const [file, setFile] = useState(null);
    const SendQuestion = async (e) => {

    const selectedFile = e.target.files[0];
    setFile(selectedFile);

        const formData = new FormData();
        formData.append('file', selectedFile);


        await axios({
            method: 'post',
            url: 'http://localhost:8000/uploadfile/',
            data:formData,
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }).then((response) => {
            console.log(response.data);
        }).catch((error) => {
            console.error("Error:", error);
        });
    };


    
  return (
    <>
        <div className='shadow bg-white d-flex nav-bar-top'>
            <div>
                <img src={AI_Planet_Logo} alt=''></img>
            </div>
            <div className='d-flex'>
                <input type='file' className='file' onChange={SendQuestion}></input>
            </div>
        </div>
    </>
  )
}
