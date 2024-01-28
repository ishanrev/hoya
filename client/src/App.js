import logo from './logo.svg';
import { useState, useEffect, useRef } from "react";
import axios from 'axios'
import { Grid, Container, Typography, Card, Input, TextField, Button, Dialog, DialogTitle, InputAdornment, Rating, Collapse, IconButton, CircularProgress, Box, Stack } from '@mui/material';

import './App.css';

function ConnectionChat({ chats = [{ role: "human", content: "ye boiiii" }, { role: "assisstant", content: "less gooo boiiii" }] }) {

  const [quest, setQuest] = useState("")
  const [conversation, setConversation] = useState([])
  const [history, setHistory] = useState([])
  const scrollRef = useRef(null);
  useEffect(() => {
    if (scrollRef.current) {
        scrollRef.current.scrollIntoView({ behaviour: "smooth" });
    }
    window.scrollTo(0, 0)

}, [conversation]);

  const send = async () => {
    try {

      // let res = await axios.get("http://localhost:5000/")
      console.log(conversation)
      setQuest("")
      let res = await axios.post("http://localhost:5000/ask", { question: quest, conversation })
      if (res.data.response !== undefined) {
        // let temp = conversation
        // temp.push({ role: "human", content: res.data.question })
        // temp.push({ role: "assistant", content: res.data.response })
        setConversation([...conversation, { role: "user", content: res.data.question }, { role: "system", content: res.data.response }])
        // setHistory()
      }
      console.log(res)
    } catch (error) {
      console.log(error.message)
    }
  }

  useEffect(() => {
    // console.log('typing chat from where I want to type my friend')
  }, [])
  const sideRender = (sender) => {
    if (sender === "user") {
      return 'end'
    } else {
      return 'start'
    }

    // if (sender === 'bob') {
    //     return 'end'
    // } else {
    //     return 'start'
    // }
  }
  const colourRender = (sender) => {
    if (sender === 'user') {
      return '#3C486B'
    } else {
      return 'white'
    }

    // if (sender === 'bob') {
    //     return '#3f51b5'
    // } else {
    //     return '#f5f5f5'
    // }
  }
  const textColourRender = (sender) => {
    if (sender === "user") {
      return 'white'
    } else {
      return 'black'
    }

    // if (sender === 'bob') {
    //     return 'white'
    // } else {
    //     return 'black'
    // }
  }
  // const chatParent = useRef < HTMLDivElement > (null);
  useEffect(() => {

  }, [])
  // useEffect(() => {
  //     if (scrollRef.current) {
  //         scrollRef.current.scrollIntoView({ behaviour: "smooth" });
  //     }
  //     window.scrollTo(0, 0)

  // }, [chats]);
  // useEffect(() => {
  //     const domNode = chatParent.current;
  //     if (domNode) {
  //         domNode.scrollTop = domNode.scrollHeight;
  //     }
  // })
  return (
    <>


      <Box sx={{ overflowY: 'scroll', height: '75%', borderRadius: '10px' }}>
        {conversation.map((ch, index) => {
          const { role, content } = ch
          return (
            <>
              <Stack
                direction="row"
                // justifyContent={"flex-" + sideRender(sender)'}
                justifyContent={"flex-" + sideRender(role)}
                // justifyContent={"flex-end"}
                alignItems="center"
                spacing={2}

              >


                <Box component='div' sx={{
                  px: "1rem",
                  py: "0.5rem", my: "0.1rem", wordWrap: 'break-word', overflow: "hidden"
                  , maxWidth: "40%", color: textColourRender(role),
                  backgroundColor: colourRender(role),
                  borderRadius: "10px"
                }}>
                  <Typography noWrap sx={{ whiteSpace: "break-spaces" }}>{content}</Typography>
                </Box>

              </Stack>
              <>
              </>
            </>
          )
        })}

      </Box>

      <Box className=" absolute top-[75vh]" sx={{ width: '85vw', height: "12vh", px: "1rem", pt: "1rem", backgroundColor: "#fafafa", borderRadius: "10px" }}>
        {/* <ConnectionChat chat={chat} /> */}
        <Stack direction={'row'} spacing={1} justifyContent={'space-between'} >

          <Input multiline sx={{ ':after': { borderBottomColor: '#3C486B' } }}
            rows={2} fullWidth value={quest} onChange={(e) => { setQuest(e.target.value); }} />


          <Button sx={{ maxHeight: '40px', backgroundColor: "#3C486B" }} variant="contained"
            onClick={send} >
            Send
          </Button>

        </Stack>

      <div ref={scrollRef}   >
                </div>
      </Box>


    </>
  )
}

function App() {

  const [conversation, setConversation] = useState([])
  const [question, setQuestion] = useState("What is the stomata?")

  let fetchData = async () => {
    try {

      // let res = await axios.get("http://localhost:5000/")
      let res = await axios.post("http://localhost:5000/ask", { question: question, conversation: conversation })
      console.log(res)
    } catch (error) {
      console.log(error.message)
    }
  }
  useEffect(() => {
    fetchData()
  }, [])

  return (
    <div className="App">
      <header className="App-header px-24 ">
        <div className='w-full bg-gray-300 rounded-lg h-[80vh] p-4'>

          {/* <Typography className='text-lg text-red-200'> bob</Typography> */}
          <ConnectionChat />
        </div>
      </header>
    </div>
  );
}

export default App;
