import './App.css';
import React, { Component } from 'react';
import ChatBot from './components';
import { ThemeProvider } from 'styled-components';

class App extends Component {
  constructor(props){
    super(props);
    this.state ={
      response: '',
    }
    this.theme = {
      background: 'rgba(255, 255, 255, 1)',
      fontFamily: 'Helvetica Neue',
      'border-radius': '10px',
      headerBgColor: 'rgb(70, 138, 150, 1)',
      headerFontColor: '#fff',
      headerFontSize: '25px',
      botBubbleColor: '#fff',
      botFontColor: '#4a4a4a',
      userBubbleColor: 'rgb(70, 138, 150, 0.85)',
      userFontColor: '#fff',
    };
  };

  async predict(text){
    const url = "http://localhost:8000/response";
    const bodyData = JSON.stringify({
      "text" : text
    });
    const reqOpt = {method: "POST", headers: {"Content-type": "application/json"}, body: bodyData};
    await fetch(url, reqOpt)
    .then((resp)=>resp.json())
    .then((respJ)=> {
      this.setState({
        response:respJ.label,
      }, ()=>{
        console.log(respJ.label)

      })
    });
  };

  async conversationUpdate(conv){
    var conver = "";
    for (let i = 0; i < conv.length; i++) {
      conver += conv[i] + "\n";
    }
    const url = "http://localhost:8000/conversation";
    const bodyData = JSON.stringify({
      "conversation" : conver
    });
    const reqOpt = {method: "POST", headers: {"Content-type": "application/json"}, body: bodyData};
    await fetch(url, reqOpt)
    .then((resp) => resp.json())
    .then((respJ) => {
      console.log('Conversation updated!')
    });
  };

  render(){
    return (
      <div className = "App">
        <header className = "App-header">
        <ThemeProvider theme = {this.theme}>
          <ChatBot
            headerTitle = 'Covid19 chatbot'
            botDelay = {3000}
            userDelay = {1500}
            width = {'500px'}
            height = {'650px'}
            floating = {true}
            steps = {[
              {
                id: 'start',
                message: () => {
                  return 'Chào bạn, mình là chatbot hỗ trợ giải đáp thắc mắc cho người dân thành phố Hồ Chí Minh đang phải cách ly tại nhà vì Covid-19. Bạn cần tư vấn về vấn đề gì vậy?'
                },
                trigger: 'user',
              },
              {
                id: 'user',
                user: true,
                trigger: (value)=>{
                  if(!value.value){
                    return 'user'
                  }
                  this.predict(value.value)
                  return 'bot'
                }
              },
              {
                // this step to wait to states updated
                id: 'bot',
                message: 'gypERR!sackError:Col o id nyVisualStuio nstallationtouse',
                trigger: 'reply'
              },
              {
                id: 'reply',
                message: (value)=>{
                  console.log(value.steps);
                  console.log(this.state.response)
                  return this.state.response;
                },
                trigger: 'user'
              }
            ]}
          />
          </ThemeProvider>
        </header>
      </div>
    );
  }
}
export default App;
