from cryptography.hazmat.primitives.asymmetric import x25519
from XEdDSA import sign

class User():

  def __init__(self, name, MAX_OPK_NUM):
      self.name = name
      # Identity key
      self.IK_s = x25519.X25519PrivateKey.generate()
      self.IK_p = self.IK_s.public_key()
      # Signed pre key, regenerate regularly (days/weeks)
      self.SPK_s = x25519.X25519PrivateKey.generate()
      self.SPK_p = self.IK_s.public_key()
      # Sign pre key with identity key to verify
      self.SPK_sig = sign(IK_s, SPK_p)
      # One time pre keys -> Used for inital handshake and then revoked, need to be regenerated as used
      self.OKPs = []
      self.OPKs_p = []
      # Generate multiple one time pre keys and send them to the server
      # So when people want to message me the server can send them the OKP
      for i in range(MAX_OPK_NUM):
          sk = x25519.X25519PrivateKey.generate()
          pk = sk.public_key()
          self.OPKs_p.append(pk)
          self.OKPs.append((sk, pk))
          # for later steps
          self.key_bundles = {}
          self.dr_keys= {}

          def publish(self):
              return {
                  'IK_p': self.IK_p,
                  'SPK_p': self.SPK_p,
                  'SPK_sig': self.SPK_sig,
                  'OPKs_p': self.OPKs_p
              }


user = User()
print(user.publish())

