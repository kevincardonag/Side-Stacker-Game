import React, {Component} from 'react'

function getOtherPlayer(player){
    return player === "x"
        ? "o"
        : "x"
}
function spanStyles(value){
    const textColor = value === "x" ? "blue": "maroon"
    const styles = {
        borderBottom: "1px solid black",
        lineHeight: "2em",
        margin: "0",
        minHeight: "20px",
        textAlign: "center",
        width: "80%",
        color: textColor,
        marginInline: "auto",
    }
    return styles
}
function labelWinStyles(value){
    const textColor = value === "x" ? "blue": "maroon"
    const styles = {
        color: textColor
    }
    return styles
}

class InputMatrix extends Component {
    constructor() {
        super();
        this.state = {
            thereIsWinner: false,
        }
    }

    handleInputChange = (indexRow, side, event) => {
        this.props.setValue(indexRow, side, this.props.player)
    }

    // rendering
    render(){
    const {board, max_movements, winner} = this.props
    return (
        <div className="InputMatriz">
            <hr style={{width: "70%"}} />
            <h1> <strong> {this.props.messageTurn} </strong> </h1>
                { winner
                    ? <div>
                        <p style={labelWinStyles(winner)}> PLAYER {winner} WON</p>
                        <p style={labelWinStyles(getOtherPlayer(winner))}> PLAYER {getOtherPlayer(winner)} LOST </p>
                      </div>
                    : <span></span>
                }
                {
                    max_movements
                    ? <div>
                        <h2> <b> no movements available</b></h2>
                      </div>
                    : <span></span>
                }
                <hr style={{width: "70%"}} />
            <div style={{ textAlign:"-webkit-center" }} className="InputMatriz__inputs-wrapper">
                <table style={{width: '50%'}} className="InputMatriz__inputs">
                    <tbody>
                        <tr>
                            <td/>
                            <td style={{textAlign: "center"}}>Board</td>
                            <td/>
                        </tr>
                    </tbody>
                </table>
                <table style={{width: '50%'}} className="InputMatriz__inputs">
                    <tbody>
                    {board.map((row, indexRow) => (
                        <tr key={indexRow} className="InputMatriz__rows">
                            <p style={{ textAlign:"center"}}>
                                <button
                                    disabled={winner || max_movements}
                                    onClick={(event) => this.handleInputChange(indexRow,"L", event)}
                                    className="InputMatriz__input"
                                    id={ `L-${indexRow}`}
                                    name={ `L-${indexRow}`}
                                >
                                    {indexRow +1 }
                                </button>
                            </p>
                            {row.map((value, indexCol) => (
                                <td key={`${indexRow}-${indexCol}`} className="InputMatriz__col" style={{width: '10%' }}>
                                    <p style={spanStyles(value)}>{value}</p>
                                </td>
                            ))}
                            <p style={{ textAlign:"center"}}>
                                <button
                                    disabled={winner || max_movements}
                                    onClick={(event) => this.handleInputChange(indexRow,"R", event)}
                                    className="InputMatriz__input"
                                    id={ `R-${indexRow}`}
                                    name={ `R-${indexRow}`}
                                >
                                {indexRow + 1}
                                </button>
                            </p>
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