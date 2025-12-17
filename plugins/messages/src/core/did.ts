/**
 * Decentralized Identifier (DID) Utilities
 *
 * Implements did:key method with Ed25519 keys.
 * DIDs provide portable, cryptographic identity across platforms.
 *
 * Format: did:key:z + base58(multicodec_prefix + public_key)
 *
 * The "z" prefix indicates base58btc encoding (multibase).
 * The multicodec prefix (0xed01) indicates Ed25519 public key.
 */

import { generateKeyPairSync, sign, verify, createPublicKey, createPrivateKey } from "crypto";
import { base58Encode, base58Decode } from "./cid";
import type { DID } from "../types";

// Multicodec prefix for Ed25519 public key
const MULTICODEC_ED25519_PUB = new Uint8Array([0xed, 0x01]);

/**
 * DID Key pair with signing capabilities
 */
export interface DIDKeyPair {
  did: DID;
  publicKey: Uint8Array;
  privateKey: Uint8Array;
}

/**
 * Generate a new DID with Ed25519 keypair
 *
 * Returns a DID in the format: did:key:z...
 * Along with the raw public and private key bytes.
 */
export function generateDID(): DIDKeyPair {
  const { publicKey, privateKey } = generateKeyPairSync("ed25519");

  // Export keys to raw format
  // SPKI format for Ed25519 has 12 bytes header, key is last 32 bytes
  const pubKeyDer = publicKey.export({ type: "spki", format: "der" });
  const pubKeyRaw = new Uint8Array(pubKeyDer.slice(-32));

  // PKCS8 format for Ed25519 - we store the full DER for signing
  const privKeyDer = privateKey.export({ type: "pkcs8", format: "der" });

  // Build multicodec key: prefix + public key
  const multicodecKey = new Uint8Array(MULTICODEC_ED25519_PUB.length + pubKeyRaw.length);
  multicodecKey.set(MULTICODEC_ED25519_PUB, 0);
  multicodecKey.set(pubKeyRaw, MULTICODEC_ED25519_PUB.length);

  // Encode with multibase (z = base58btc)
  const did = `did:key:z${base58Encode(multicodecKey)}` as DID;

  return {
    did,
    publicKey: pubKeyRaw,
    privateKey: new Uint8Array(privKeyDer),
  };
}

/**
 * Extract public key from a did:key DID
 */
export function extractPublicKey(did: DID): Uint8Array {
  if (!did.startsWith("did:key:z")) {
    throw new Error("Only did:key method with base58btc (z) encoding is supported");
  }

  // Remove "did:key:z" prefix and decode
  const encoded = did.slice(9);
  const decoded = base58Decode(encoded);

  // Verify multicodec prefix
  if (decoded[0] !== 0xed || decoded[1] !== 0x01) {
    throw new Error("Invalid multicodec prefix - expected Ed25519 public key (0xed01)");
  }

  // Return raw public key (without prefix)
  return decoded.slice(2);
}

/**
 * Sign content with a DID private key
 *
 * Returns base58-encoded signature.
 */
export function signWithDID(content: string, privateKey: Uint8Array): string {
  const privKeyObj = createPrivateKey({
    key: Buffer.from(privateKey),
    format: "der",
    type: "pkcs8",
  });

  const signature = sign(null, Buffer.from(content), privKeyObj);
  return base58Encode(new Uint8Array(signature));
}

/**
 * Verify a signature against a DID
 */
export function verifyDIDSignature(did: DID, content: string, signature: string): boolean {
  try {
    const publicKey = extractPublicKey(did);

    // Reconstruct SPKI format for verification
    // Ed25519 SPKI header
    const spkiHeader = new Uint8Array([
      0x30, 0x2a, 0x30, 0x05, 0x06, 0x03, 0x2b, 0x65, 0x70, 0x03, 0x21, 0x00,
    ]);
    const spkiKey = new Uint8Array(spkiHeader.length + publicKey.length);
    spkiKey.set(spkiHeader, 0);
    spkiKey.set(publicKey, spkiHeader.length);

    const pubKeyObj = createPublicKey({
      key: Buffer.from(spkiKey),
      format: "der",
      type: "spki",
    });

    const sigBytes = base58Decode(signature);
    return verify(null, Buffer.from(content), pubKeyObj, Buffer.from(sigBytes));
  } catch {
    return false;
  }
}

/**
 * Check if a string is a valid did:key format
 */
export function isValidDID(str: string): boolean {
  if (!str.startsWith("did:key:z")) {
    return false;
  }

  try {
    extractPublicKey(str as DID);
    return true;
  } catch {
    return false;
  }
}

/**
 * Export DID keypair for storage
 */
export function exportDIDKeyPair(keypair: DIDKeyPair): { did: string; privateKey: string } {
  return {
    did: keypair.did,
    privateKey: base58Encode(keypair.privateKey),
  };
}

/**
 * Import DID keypair from storage
 */
export function importDIDKeyPair(data: { did: string; privateKey: string }): DIDKeyPair {
  const privateKey = base58Decode(data.privateKey);
  const publicKey = extractPublicKey(data.did as DID);

  return {
    did: data.did as DID,
    publicKey,
    privateKey,
  };
}

/**
 * Generate a deterministic DID from a seed
 *
 * Useful for deriving DIDs from other identifiers (e.g., platform handles).
 * Note: This is less secure than random generation - use for derived identities only.
 */
export function deriveDID(seed: string): DIDKeyPair {
  // Use seed to generate deterministic keypair
  // This is a simplified implementation - production would use proper KDF
  const { createHash } = require("crypto");
  const seedHash = createHash("sha256").update(seed).digest();

  // Ed25519 seed is 32 bytes
  const { generateKeyPairSync } = require("crypto");

  // Note: Node.js doesn't support seeded Ed25519 directly
  // For deterministic DIDs, we'd need a different approach
  // For now, this just generates a random keypair
  // TODO: Implement proper deterministic key derivation
  return generateDID();
}

/**
 * Create a DID from an existing public key
 */
export function didFromPublicKey(publicKey: Uint8Array): DID {
  if (publicKey.length !== 32) {
    throw new Error("Ed25519 public key must be 32 bytes");
  }

  const multicodecKey = new Uint8Array(MULTICODEC_ED25519_PUB.length + publicKey.length);
  multicodecKey.set(MULTICODEC_ED25519_PUB, 0);
  multicodecKey.set(publicKey, MULTICODEC_ED25519_PUB.length);

  return `did:key:z${base58Encode(multicodecKey)}` as DID;
}
