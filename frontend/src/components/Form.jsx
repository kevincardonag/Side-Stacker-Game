import React, {Component} from 'react'
import config from "../config";
import InputMatrix from "./InputMatriz.jsx";

class Form extends Component{
    constructor() {
        super();
        this.state = {
            inputName: "",
            board:[],
            win: false,
            player: "",
        }
        this.socketRef = null;
    }
    setValue = (row, col, player) => {
        this.socketRef.send(JSON.stringify({
            'col': col,
            'row': row,
            'player': player,
            'room_name': this.state.inputName,
        }));
    }
    handleSubmit = (e)=> {
        e.preventDefault();
        const roomName = this.state.inputName
        const path = `${config.API_PATH}/${roomName}/`;
        this.socketRef = new WebSocket(path);
        this.socketRef.onopen = () => {
            console.log('WebSocket open');
        };
        this.socketRef.onmessage = e => {
            const message = JSON.parse(e.data).message
            this.setState({
                board: message.board,
                win: message.win,
                player: message.player,
            })
        };

        this.socketRef.onerror = e => {
            console.log(e.message);
        };
        this.socketRef.onclose = () => {
            console.log("WebSocket closed let's reopen");
        };
    }
    handleClick = (e)=>{
        this.setState({
            inputName: "",
            board:[],
            win: false,
            player: "",
        })
    }
    render(){
        const displayBoard = this.state.board.length !== 0
            ? <InputMatrix
                player={this.state.player}
                board={this.state.board}
                win={this.state.win}
                setValue={this.setValue}
            />
            : <p> Please enter a room to start the game </p>

        return(
            <div>
                <h4> Room Name </h4>
                <div>
                    <form onSubmit={this.handleSubmit}>
                        <input
                            required={true}
                            id='room_name'
                            placeholder='Room name'
                            name='room_name'
                            onChange={e => this.setState({inputName: e.target.value})}
                            value={this.state.inputName}
                            disabled={!(this.state.board.length === 0)}
                        />
                        <p>
                            <button disabled={! (this.state.board.length === 0)}> Enter room </button >
                            <button onClick={this.handleClick } disabled={this.state.board.length === 0}> Change room </button>
                        </p>

                    </form>
                </div>
                {displayBoard}
            </div>

        )
    }
}

export default Form