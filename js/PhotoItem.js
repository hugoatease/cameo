var React = require('react');
var ReactDOM = require('react-dom');

module.exports = React.createClass({
    componentDidMount: function() {
        $(ReactDOM.findDOMNode(this)).magnificPopup({
            items: {
                src: this.props.media.url,
                type: 'image'
            }
        })
    },

    render: function() {
        return (
            <div className="column">
                <img className="thumbnail" src={this.props.media.url} />
            </div>
        )
    }
})