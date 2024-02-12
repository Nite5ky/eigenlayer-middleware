
methods {
    //// External Calls
	// external calls to StakeRegistry
    function _.quorumCount() external => DISPATCHER(true);
    function _.getCurrentTotalStake(uint8 quorumNumber) external => DISPATCHER(true);
    function _.getCurrentStake(bytes32 operatorId, uint8 quorumNumber) external => DISPATCHER(true);
    // function _.registerOperator(address, bytes32, bytes) external => DISPATCHER(true);
    function _.registerOperator(address, bytes32, bytes) external => NONDET;
    function _.deregisterOperator(bytes32, bytes) external => NONDET;

    // external calls to BlsApkRegistry
    // function _.registerOperator(address, bytes, BN254.G1Point) external => DISPATCHER(true);
    function _.registerOperator(address, bytes) external => NONDET;
    function _.deregisterOperator(address, bytes) external => NONDET;
    function _.pubkeyHashToOperator(bytes32) external => DISPATCHER(true);

    // external calls to IndexRegistry
    // function _.registerOperator(bytes32, bytes) external => DISPATCHER(true);
    function _.registerOperator(bytes32, bytes) external => NONDET;
    function _.deregisterOperator(bytes32, bytes, bytes32[]) external => NONDET;

	// external calls to ServiceManager
    function _.registerOperatorToAVS(address, ISignatureUtils.SignatureWithSaltAndExpiry) external => DISPATCHER(true);
    function _.deregisterOperatorFromAVS(address) external => DISPATCHER(true);
    // function _.recordLastStakeUpdateAndRevokeSlashingAbility(address, uint256) external => DISPATCHER(true);
    // function _.registerOperatorToAVS(address, ISignatureUtils.SignatureWithSaltAndExpiry) external => NONDET;
    // function _.deregisterOperatorToAVS(address) external => NONDET;

    // external calls to AVSDirectory
    function _.registerOperatorToAVS(address, ISignatureUtils.SignatureWithSaltAndExpiry) external => DISPATCHER(true);
    function _.deregisterOperatorFromAVS(address) external => DISPATCHER(true);


    // external calls to ERC1271 (can import OpenZeppelin mock implementation)
    // isValidSignature(bytes32 hash, bytes memory signature) returns (bytes4 magicValue) => DISPATCHER(true)
    // function _.isValidSignature(bytes32, bytes) external => DISPATCHER(true);
    function _.isValidSignature(bytes32, bytes) external => NONDET;

    //envfree functions
    function OPERATOR_CHURN_APPROVAL_TYPEHASH() external returns (bytes32) envfree;
    function serviceManager() external returns (address) envfree;
    function blsApkRegistry() external returns (address) envfree;
    function stakeRegistry() external returns (address) envfree;
    function indexRegistry() external returns (address) envfree;
    function churnApprover() external returns (address) envfree;
    function isChurnApproverSaltUsed(bytes32) external returns (bool) envfree;
    function getOperatorSetParams(uint8 quorumNumber) external returns (IRegistryCoordinator.OperatorSetParam) envfree;
    function getOperator(address operator) external returns (IRegistryCoordinator.OperatorInfo) envfree;
    function getOperatorId(address operator) external returns (bytes32) envfree;
    function getOperatorStatus(address operator) external returns (IRegistryCoordinator.OperatorStatus) envfree;
    function getQuorumBitmapIndicesAtBlockNumber(uint32 blockNumber, bytes32[] operatorIds)
        external returns (uint32[]) envfree;
    function getQuorumBitmapAtBlockNumberByIndex(bytes32 operatorId, uint32 blockNumber, uint256 index) external returns (uint192) envfree;
    function getQuorumBitmapUpdateByIndex(bytes32 operatorId, uint256 index)
        external returns (IRegistryCoordinator.QuorumBitmapUpdate) envfree;
    function getCurrentQuorumBitmap(bytes32 operatorId) external returns (uint192) envfree;
    function getQuorumBitmapHistoryLength(bytes32 operatorId) external returns (uint256) envfree;
    function registries(uint256) external returns (address) envfree;
    function numRegistries() external returns (uint256) envfree;
    function calculateOperatorChurnApprovalDigestHash(
        address registeringOperator,
        bytes32 registeringOperatorId,
        IRegistryCoordinator.OperatorKickParam[] operatorKickParams,
        bytes32 salt,
        uint256 expiry
    ) external returns (bytes32) envfree;

    // harnessed functions
    function bytesArrayContainsDuplicates(bytes bytesArray) external returns (bool) envfree;
    function bytesArrayIsSubsetOfBitmap(uint256 referenceBitmap, bytes arrayWhichShouldBeASubsetOfTheReference) external returns (bool) envfree;
}

// If my Operator status is REGISTERED ⇔ my quorum bitmap MUST BE nonzero
invariant registeredOperatorsHaveNonzeroBitmaps(address operator)
    getOperatorStatus(operator) == IRegistryCoordinator.OperatorStatus.REGISTERED <=>
        getCurrentQuorumBitmap(getOperatorId(operator)) != 0;

// if two operators have different addresses, then they have different IDs
// excludes the case in which the operator is not registered, since then they can both have ID zero (the default)
invariant operatorIdIsUnique(address operator1, address operator2)
    operator1 != operator2 =>
        (getOperatorStatus(operator1) == IRegistryCoordinator.OperatorStatus.REGISTERED => getOperatorId(operator1) != getOperatorId(operator2));

definition methodCanModifyBitmap(method f) returns bool =
    f.selector == sig:registerOperator(
      bytes,
      string,
      IBLSApkRegistry.PubkeyRegistrationParams,
      ISignatureUtils.SignatureWithSaltAndExpiry
    ).selector
    || f.selector == sig:registerOperatorWithChurn(
        bytes,
        string,
        IBLSApkRegistry.PubkeyRegistrationParams,
        IRegistryCoordinator.OperatorKickParam[],
        ISignatureUtils.SignatureWithSaltAndExpiry,
        ISignatureUtils.SignatureWithSaltAndExpiry
    ).selector;

definition methodCanAddToBitmap(method f) returns bool =
    f.selector == sig:registerOperator(
      bytes,
      string,
      IBLSApkRegistry.PubkeyRegistrationParams,
      ISignatureUtils.SignatureWithSaltAndExpiry
    ).selector
    || f.selector == sig:registerOperatorWithChurn(
        bytes,
        string,
        IBLSApkRegistry.PubkeyRegistrationParams,
        IRegistryCoordinator.OperatorKickParam[],
        ISignatureUtils.SignatureWithSaltAndExpiry,
        ISignatureUtils.SignatureWithSaltAndExpiry
    ).selector;

// `registerOperatorWithChurn` with kick params also meets this definition due to the 'churn' mechanism
definition methodCanRemoveFromBitmap(method f) returns bool =
    f.selector == sig:registerOperatorWithChurn(
        bytes,
        string,
        IBLSApkRegistry.PubkeyRegistrationParams,
        IRegistryCoordinator.OperatorKickParam[],
        ISignatureUtils.SignatureWithSaltAndExpiry,
        ISignatureUtils.SignatureWithSaltAndExpiry
    ).selector
    || f.selector == sig:deregisterOperator(bytes).selector
    || f.selector == sig:ejectOperator(address, bytes).selector;

// verify that quorumNumbers provided as an input to deregister operator MUST BE a subset of the operator’s current quorums
rule canOnlyDeregisterFromExistingQuorums(address operator) {
    requireInvariant registeredOperatorsHaveNonzeroBitmaps(operator);

    // TODO: store this status, verify that all calls to `deregisterOperator` *fail* if the operator is not registered first!
    require(getOperatorStatus(operator) == IRegistryCoordinator.OperatorStatus.REGISTERED);

    uint256 bitmapBefore = getCurrentQuorumBitmap(getOperatorId(operator));

    bytes quorumNumbers;
    env e;

    deregisterOperator(e, quorumNumbers);

    // if deregistration is successful, verify that `quorumNumbers` input was proper
    if (getOperatorStatus(operator) != IRegistryCoordinator.OperatorStatus.REGISTERED) {
        assert(bytesArrayIsSubsetOfBitmap(bitmapBefore, quorumNumbers));
    } else {
        assert(true);
    }
}

/* TODO: this is a Work In Progress
rule canOnlyModifyBitmapWithSpecificFunctions(address operator) {
    requireInvariant registeredOperatorsHaveNonzeroBitmaps(operator);
    uint256 bitmapBefore = getCurrentQuorumBitmap(getOperatorId(operator));
    // prepare to perform arbitrary function call
    method f;
    env e;
    // TODO: need to ensure that if the function can modify the bitmap, then we are using the operator as an input
    if (!methodCanModifyBitmap(f)) {
        // perform arbitrary function call
        calldataarg arg;
        f(e, arg);
        uint256 bitmapAfter = getCurrentQuorumBitmap(getOperatorId(operator));
        assert(bitmapAfter == bitmapBefore);
    } else if (
        f.selector == sig:registerOperatorWithCoordinator(bytes, bytes).selector
    ) {
        if (e.msg.sender != operator) {
            uint256 bitmapAfter = getCurrentQuorumBitmap(getOperatorId(operator));
            assert(bitmapAfter == bitmapBefore);
        }
    }

        // if method did not remove from bitmap, it must have added
        if (bitmapAfter & bitmapBefore == bitmapBefore) {
            assert(methodCanAddToBitmap(f));
        } else {
            assert(methodCanRemoveFromBitmap(f));
        }
    }
}
*/