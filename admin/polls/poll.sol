pragma solidity >=0.4.22 <0.6.0;
contract pollBooth {
    
    address admin;
    uint256[] CandidateVotes;
    int facGroupSize;
    uint256 commitDeadline;     // time (in secs) from start of poll to actual commit Deadline
    uint256 revealDeadline;     // time (in secs) from start of poll to actual reveal Deadline
    bytes32[] revealArr;        // might need to use string [] everywhere for this
    
    mapping (bytes32 => int) commitRevealCount;
    
    uint256 contractDeployTime; 
    
    constructor(uint8 _numProposals, uint8 _facGroupSize, uint256 _commitDeadline, uint256 _revealDeadline) public {
        admin = msg.sender;
        CandidateVotes.length = _numProposals;
        facGroupSize = _facGroupSize;
        contractDeployTime = now;
        commitDeadline = _commitDeadline + contractDeployTime * 1 seconds;
        revealDeadline = _revealDeadline + contractDeployTime * 1 seconds;
    }
    
    function commitVote(bytes32 Vote) public {
        require(msg.sender == admin, "Only administrator can do any transaction with pollBooth contract.");
        require(now <= commitDeadline, "Commit Deadline Over");
        
        commitRevealCount[Vote] = 1;
    }
    
    function revealVote(bytes32 Vote) public {
        require(msg.sender == admin, "Only administrator can do any transaction with pollBooth contract.");
        require(now >= commitDeadline, "You cannot Reveal before end of Commit Period");
        require(now <= revealDeadline, "Reveal Deadline Over");
        
        revealArr.push(Vote);
    }
    
    function countVotes() public {
        require(msg.sender == admin, "Only administrator can do any transaction with pollBooth contract.");
        require(now > revealDeadline, "You cannot start vote counting before end of Reveal Period");
        
        for (uint i = 0; i < revealArr.length; i++) {
            bytes32 commitVal = sha256(abi.encode(revealArr[i]));
            if (commitRevealCount[commitVal] == 1) {
                commitRevealCount[commitVal]++;
                
                bytes32 temp = bytes32(uint256(revealArr[i])) & bytes32(uint256(0xff));
                uint256 Candidate = uint256(temp);
                CandidateVotes[Candidate]++;
            }
        }
    }
    
    function voteCountCandidate(uint256 Candidate) public view returns (uint256) {
        require(msg.sender == admin, "Only administrator can do any transaction with pollBooth contract.");
        require(now > revealDeadline, "You cannot check vote count before end of Reveal Period");
        return CandidateVotes[Candidate];
    }   
}