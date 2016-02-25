var React = require('react');
var ReactDOM = require('react-dom');
var request = require('superagent');

var Cameo = React.createClass({
    getDefaultProps: function() {
        return {
            cameo: window.location.origin,
            gridClass: "row small-up-2 medium-up-4 large-up-6",
            limit: 5,
            refresh_interval: 15
        }
    },

    getInitialState: function() {
        return {
            medias: [],
            max_index: this.props.limit
        }
    },

    componentDidMount: function() {
        request.get(this.props.cameo + '/api/media').end(function(err, res) {
            if (err) return;
            this.setState({
                medias: res.body
            });
        }.bind(this));
    },

    loadMore: function() {
        if (this.state.max_index + this.props.limit > this.state.medias.length) {
            this.setState({
                max_index: this.state.medias.length
            });
        }
        else {
            this.setState({
                max_index: this.state.max_index + this.props.limit
            });
        }
    },

    render: function() {
        return (
            <div>
                <div className={this.props.gridClass}>
                    {function() {
                        return this.state.medias.slice(0, this.state.max_index).map(function(media) {
                            return (
                                <div className="column">
                                    <img className="thumbnail" src={media.url} />
                                </div>
                            );
                        }.bind(this));
                    }.call(this)}
                </div>
                <button className="button expanded success" onClick={this.loadMore}>Plus de photos</button>
            </div>
        );
    }
});

module.exports = function(container, props) {
    ReactDOM.render(<Cameo {...props} />, container);
}