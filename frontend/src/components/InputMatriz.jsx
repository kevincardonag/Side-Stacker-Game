import React, {Component} from 'react'

function getOtherPlayer(player){
    return player == "x"
        ? "o"
        : "x"
}

class InputMatrix extends Component {
    constructor() {
        super();
        this.state = {
            thereIsWinner: false,
        }
    }

    handleInputChange = (indexRow, indexCol, e) => {
        if(e.target.value === this.props.player ) {
            this.props.setValue(indexRow, indexCol, e.target.value)
        }else{
            this.setState({thereIsWinner: true })
        }
    }

    // rendering
    render(){
    const {board, win, player} = this.props
    return (
        <div className="InputMatriz">
            <h3 > Turn for the player: <strong> {player} </strong></h3>
                { win
                    ? <div>
                        <p style={{color: 'green'}}> PLAYER {player} WON</p>
                        <p style={{color: 'red'}}> PLAYER {getOtherPlayer(player)} LOSE</p>
                      </div>
                    : <span></span>
                }

            <div style={{ textAlign:"-webkit-center" }} className="InputMatriz__inputs-wrapper">
                <table style={{width: '50%', }} className="InputMatriz__inputs">
                    <tbody>
                    {board.map((row, indexRow) => (
                        <tr key={indexRow} className="InputMatriz__rows">
                            {row.map((value, indexCol) => (
                                <td key={`${indexRow}-${indexCol}`} className="InputMatriz__col" style={{width: '10%' }}>
                                    <input  style={{width: '80%' }}
                                        className="InputMatriz__input"
                                        id={`${indexRow}-${indexCol}`}
                                        name={`${indexRow}-${indexCol}`}
                                        value={value}
                                        disabled={!!value || win}
                                        onChange={(e) => this.handleInputChange(indexRow, indexCol, e)}
                                    />
                                </td>
                            ))}
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
        </div>
    )
    }
}

export default InputMatrix