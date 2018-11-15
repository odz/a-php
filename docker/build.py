import argparse
import subprocess
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', dest='username', required=True, type=str)
    parser.add_argument('--fullname', dest='fullname', required=True, type=str)
    parser.add_argument('--email', dest='email', required=True, type=str)
    parser.add_argument('--genkey', dest='genkey', action='store_true')

    args = parser.parse_args()
    if args.genkey:
        gen_keys(args.email)
    gen_abuild_conf(args.username, args.email)
    build_image(args)
    os.remove('abuild.conf')

def build_image(args):
    for name in ('dev', 'build'):
        tag = 'aphp-%s' % name
        dockerfile = 'Dockerfile.%s' % name

        cmd = ['docker', 'build', '-t', tag, '-f', dockerfile]
        for key in ['username', 'fullname', 'email']:
            cmd.extend(['--build-arg', '%s=%s' % (key, getattr(args, key))])
        cmd.append('.')
        subprocess.run(cmd)

def gen_keys(email):
    privkey = '%s.rsa' % email
    pubkey = '%s.rsa.pub' % email
    subprocess.run(['openssl', 'genrsa', '-out', privkey])
    subprocess.run(['openssl', 'rsa', '-in', privkey, '-pubout', '-out', pubkey])

def gen_abuild_conf(username, email):
    with open('abuild.conf', 'w') as fp:
        print('PACKAGER_PRIVKEY="/home/%s/.abuild/%s.rsa"' % (username, email), file=fp)

if __name__ == '__main__':
    main()
