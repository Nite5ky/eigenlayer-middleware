// // SPDX-License-Identifier: BUSL-1.1
// pragma solidity ^0.8.12;
// 
// import "eigenlayer-contracts/src/contracts/interfaces/IAVSDirectory.sol";
// 
// contract AVSDirectoryMock /*is IAVSDirectory*/ {
//     /**
//      * @notice Called by an AVS to create a list of new operatorSets.
//      *
//      * @param operatorSetIds The IDs of the operator set to initialize.
//      *
//      * @dev msg.sender must be the AVS.
//      * @dev The AVS may create operator sets before it becomes an operator set AVS.
//      */
//     function createOperatorSets(uint32[] calldata operatorSetIds) external {}
// 
//     /**
//      * @notice Sets the AVS as an operator set AVS, preventing legacy M2 operator registrations.
//      *
//      * @dev msg.sender must be the AVS.
//      */
//     function becomeOperatorSetAVS() external {}
// 
//     /**
//      * @notice Called by an AVS to migrate operators that have a legacy M2 registration to operator sets.
//      *
//      * @param operators The list of operators to migrate
//      * @param operatorSetIds The list of operatorSets to migrate the operators to
//      *
//      * @dev The msg.sender used is the AVS
//      * @dev The operator can only be migrated at most once per AVS
//      * @dev The AVS can no longer register operators via the legacy M2 registration path once it begins migration
//      * @dev The operator is deregistered from the M2 legacy AVS once migrated
//      */
//     function migrateOperatorsToOperatorSets(
//         address[] calldata operators,
//         uint32[][] calldata operatorSetIds
//     ) external {}
// 
//     /**
//      *  @notice Called by AVSs to add an operator to list of operatorSets.
//      *
//      *  @param operator The address of the operator to be added to the operator set.
//      *  @param operatorSetIds The IDs of the operator sets.
//      *  @param operatorSignature The signature of the operator on their intent to register.
//      *
//      *  @dev msg.sender is used as the AVS.
//      *  @dev The operator must not have a pending deregistration from the operator set.
//      */
//     function registerOperatorToOperatorSets(
//         address operator,
//         uint32[] calldata operatorSetIds,
//         ISignatureUtils.SignatureWithSaltAndExpiry memory operatorSignature
//     ) external {}
// 
//     /**
//      *  @notice Called by AVSs to remove an operator from an operator set.
//      *
//      *  @param operator The address of the operator to be removed from the operator set.
//      *  @param operatorSetIds The IDs of the operator sets.
//      *
//      *  @dev msg.sender is used as the AVS.
//      */
//     function deregisterOperatorFromOperatorSets(
//         address operator,
//         uint32[] calldata operatorSetIds
//     ) external {}
// 
//     /**
//      * @notice Called by an operator to deregister from an operator set
//      *
//      * @param operator The operator to deregister from the operatorSets.
//      * @param avs The address of the AVS to deregister the operator from.
//      * @param operatorSetIds The IDs of the operator sets.
//      * @param operatorSignature the signature of the operator on their intent to deregister or empty if the operator itself is calling
//      *
//      * @dev if the operatorSignature is empty, the caller must be the operator
//      * @dev this will likely only be called in case the AVS contracts are in a state that prevents operators from deregistering
//      */
//     function forceDeregisterFromOperatorSets(
//         address operator,
//         address avs,
//         uint32[] calldata operatorSetIds,
//         ISignatureUtils.SignatureWithSaltAndExpiry memory operatorSignature
//     ) external {}
// 
//     /**
//      * @notice Called by an avs to register an operator with the avs.
//      * @param operator The address of the operator to register.
//      * @param operatorSignature The signature, salt, and expiry of the operator's signature.
//      */
//     function registerOperatorToAVS(
//         address operator,
//         ISignatureUtils.SignatureWithSaltAndExpiry memory operatorSignature
//     ) external {}
// 
//     /**
//      * @notice Called by an avs to deregister an operator with the avs.
//      * @param operator The address of the operator to deregister.
//      */
//     function deregisterOperatorFromAVS(address operator) external {}
// 
//     /**
//      * @notice Called by an AVS to emit an `AVSMetadataURIUpdated` event indicating the information has updated.
//      * @param metadataURI The URI for metadata associated with an AVS
//      * @dev Note that the `metadataURI` is *never stored * and is only emitted in the `AVSMetadataURIUpdated` event
//      */
//     function updateAVSMetadataURI(string calldata metadataURI) external {}
// 
//     /**
//      * @notice Called by an operator to cancel a salt that has been used to register with an AVS.
//      *
//      * @param salt A unique and single use value associated with the approver signature.
//      */
//     function cancelSalt(bytes32 salt) external {}
// 
//     /**
//      * @notice Returns whether or not the salt has already been used by the operator.
//      * @dev Salts is used in the `registerOperatorToAVS` function.
//      */
//     function operatorSaltIsSpent(address operator, bytes32 salt) external view returns (bool) {}
// 
//     function isMember(
//         address avs,
//         address operator,
//         uint32 operatorSetId
//     ) external view returns (bool) {}
// 
//     /**
//      * @notice Calculates the digest hash to be signed by an operator to register with an AVS
//      * @param operator The account registering as an operator
//      * @param avs The AVS the operator is registering to
//      * @param salt A unique and single use value associated with the approver signature.
//      * @param expiry Time after which the approver's signature becomes invalid
//      */
//     function calculateOperatorAVSRegistrationDigestHash(
//         address operator,
//         address avs,
//         bytes32 salt,
//         uint256 expiry
//     ) external view returns (bytes32) {}
// 
//     /**
//      * @notice Calculates the digest hash to be signed by an operator to register with an operator set.
//      *
//      * @param avs The AVS that operator is registering to operator sets for.
//      * @param operatorSetIds An array of operator set IDs the operator is registering to.
//      * @param salt A unique and single use value associated with the approver signature.
//      * @param expiry Time after which the approver's signature becomes invalid.
//      */
//     function calculateOperatorSetRegistrationDigestHash(
//         address avs,
//         uint32[] calldata operatorSetIds,
//         bytes32 salt,
//         uint256 expiry
//     ) external view returns (bytes32) {}
// 
//     /**
//      * @notice Calculates the digest hash to be signed by an operator to force deregister from an operator set.
//      *
//      * @param avs The AVS that operator is deregistering from.
//      * @param operatorSetIds An array of operator set IDs the operator is deregistering from.
//      * @param salt A unique and single use value associated with the approver signature.
//      * @param expiry Time after which the approver's signature becomes invalid.
//      */
//     function calculateOperatorSetForceDeregistrationTypehash(
//         address avs,
//         uint32[] calldata operatorSetIds,
//         bytes32 salt,
//         uint256 expiry
//     ) external view returns (bytes32) {}
// 
//     /// @notice Getter function for the current EIP-712 domain separator for this contract.
//     /// @dev The domain separator will change in the event of a fork that changes the ChainID.
//     function domainSeparator() external view returns (bytes32) {}
// 
//     /// @notice The EIP-712 typehash for the Registration struct used by the contract
//     function OPERATOR_AVS_REGISTRATION_TYPEHASH() external view returns (bytes32) {}
// 
//     /// @notice The EIP-712 typehash for the OperatorSetRegistration struct used by the contract.
//     function OPERATOR_SET_REGISTRATION_TYPEHASH() external view returns (bytes32) {}
// 
//     function isOperatorSetAVS(address avs) external view returns (bool) {}
// 
//     function isOperatorSet(address avs, uint32 operatorSetId) external view returns (bool) {}
// 
//     function isMember(
//         address operator,
//         IAVSDirectory.OperatorSet memory operatorSet
//     ) external view returns (bool) {}
// }
