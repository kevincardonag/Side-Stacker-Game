import React, {Component} from 'react'
import config from "../config";
import InputMatrix from "./InputMatriz.jsx";

class Form extends Component{
    constructor() {
        super();
        this.state = {
            messageTurn: "",
            inputName: "",
            board:[],
            player: "",
            max_movements: false,
            winner: null,
        }
        this.socketRef = null;
    }
    setValue = (row, side, player) => {
        this.socketRef.send(JSON.stringify({
            'side': side,
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
            let message = JSON.parse(e.data).message
            let messageTurn = JSON.parse(e.data).message_turn
            if (message !== undefined){
                this.setState({
                    board: message.board,
                    player: message.player,
                    max_movements: message.max_movements,
                    winner: message.winner,
                })
            }
            if (messageTurn !== undefined){
                this.setState({
                    messageTurn: messageTurn
                })
            }
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
            player: "",
            max_movements: false,
            winner: "",
        })
    }
    render(){
        const displayBoard = this.state.board.length !== 0
            ? <InputMatrix
                player={this.state.player}
                board={this.state.board}
                setValue={this.setValue}
                max_movements={this.state.max_movements}
                winner={this.state.winner}
                messageTurn={this.state.messageTurn}
            />
            : <p> Please enter a room name to start the game </p>

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
                            onChange={e => this.setState({inputName: e.target.value.replace(/ /g,'')})}
                            value={this.state.inputName}
                            disabled={!(this.state.board.length === 0)}
                        />
                        <p>
                            <button
                                disabled={! (this.state.board.length === 0)}
                            >
                                Enter room
                            </button >
                            <button
                                onClick={this.handleClick }
                                disabled={this.state.board.length === 0}
                            >
                                Change room
                            </button>
                        </p>

                    </form>
                </div>
                {displayBoard}
            </div>
        )
    }
}

export default Form