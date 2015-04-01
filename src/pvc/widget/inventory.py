"""
Docstring should go here

"""

import pyVmomi

import pvc.widget.cluster
import pvc.widget.menu
import pvc.widget.datastore
import pvc.widget.hostsystem
import pvc.widget.network
import pvc.widget.virtualmachine

__all__ = ['InventoryWidget', 'InventorySearchWidget']


class InventoryWidget(object):
    def __init__(self, agent, dialog):
        """
        Inventory widget

        Args:
            agent (VConnector): A VConnector instance
            dialog    (Dialog): A Dialog instance

        """
        self.agent = agent
        self.dialog = dialog
        self.display()

    def display(self):
        items = [
            pvc.widget.menu.MenuItem(
                tag='Clusters',
                description='Manage Clusters',
                on_select=self.cluster_menu
            ),
            pvc.widget.menu.MenuItem(
                tag='Hosts',
                description='Manage hosts',
                on_select=self.host_menu
            ),
            pvc.widget.menu.MenuItem(
                tag='VMs & Templates',
                description='Manage VMs & Templates',
                on_select=self.virtual_machine_menu
            ),
            pvc.widget.menu.MenuItem(
                tag='Datastores',
                description='Manage Datastores',
                on_select=self.datastore_menu
            ),
            pvc.widget.menu.MenuItem(
                tag='Networking',
                description='Manage Networking',
                on_select=self.network_menu
            ),
            pvc.widget.menu.MenuItem(
                tag='Search',
                description='Search Inventory',
                on_select=InventorySearchWidget,
                on_select_args=(self.agent, self.dialog)
            ),
        ]

        menu = pvc.widget.menu.Menu(
            items=items,
            dialog=self.dialog,
            title='Inventory Menu',
            text='Select an item from the inventory'
        )

        menu.display()

    def cluster_menu(self):
        self.dialog.infobox(
            text='Retrieving information ...'
        )

        view = self.agent.get_cluster_view()
        properties = self.agent.collect_properties(
            view_ref=view,
            obj_type=pyVmomi.vim.ClusterComputeResource,
            path_set=['name', 'overallStatus'],
            include_mors=True
        )
        view.DestroyView()

        items = [
            pvc.widget.menu.MenuItem(
                tag=cluster['name'],
                description=cluster['overallStatus'],
                on_select=pvc.widget.cluster.ClusterWidget,
                on_select_args=(self.agent, self.dialog, cluster['obj'])
            ) for cluster in properties
        ]

        menu = pvc.widget.menu.Menu(
            items=items,
            dialog=self.dialog,
            title='Clusters',
            text='\nSelect a cluster from the menu\n'
        )

        menu.display()

    def host_menu(self):
        self.dialog.infobox(
            text='Retrieving information ...'
        )

        view = self.agent.get_host_view()
        properties = self.agent.collect_properties(
            view_ref=view,
            obj_type=pyVmomi.vim.HostSystem,
            path_set=['name', 'runtime.connectionState'],
            include_mors=True
        )
        view.DestroyView()

        items = [
            pvc.widget.menu.MenuItem(
                tag=host['name'],
                description=host['runtime.connectionState'],
                on_select=pvc.widget.hostsystem.HostSystemWidget,
                on_select_args=(self.agent, self.dialog, host['obj'])
            ) for host in properties
        ]

        menu = pvc.widget.menu.Menu(
            items=items,
            dialog=self.dialog,
            title='Hosts',
            text='Select a host from the menu'
        )

        menu.display()

    def datastore_menu(self):
        self.dialog.infobox(
            text='Retrieving information ...'
        )

        view = self.agent.get_datastore_view()
        properties = self.agent.collect_properties(
            view_ref=view,
            obj_type=pyVmomi.vim.Datastore,
            path_set=['name', 'summary.accessible'],
            include_mors=True
        )
        view.DestroyView()

        items = [
            pvc.widget.menu.MenuItem(
                tag=ds['name'],
                description='Accessible' if ds['summary.accessible'] else 'Not Accessible',
                on_select=pvc.widget.datastore.DatastoreWidget,
                on_select_args=(self.agent, self.dialog, ds['obj'])
            ) for ds in properties
        ]

        menu = pvc.widget.menu.Menu(
            items=items,
            dialog=self.dialog,
            title='Datastores',
            text='Select a Datastore from the menu'
        )

        menu.display()

    def virtual_machine_menu(self):
        self.dialog.infobox(
            text='Retrieving information ...',
            width=40
        )

        view = self.agent.get_vm_view()
        properties = self.agent.collect_properties(
            view_ref=view,
            obj_type=pyVmomi.vim.VirtualMachine,
            path_set=['name', 'runtime.powerState'],
            include_mors=True
        )
        view.DestroyView()

        items = [
            pvc.widget.menu.MenuItem(
                tag=vm['name'],
                description=vm['runtime.powerState'],
                on_select=pvc.widget.virtualmachine.VirtualMachineWidget,
                on_select_args=(self.agent, self.dialog, vm['obj'])
            ) for vm in properties
        ]

        menu = pvc.widget.menu.Menu(
            items=items,
            dialog=self.dialog,
            title='Virtual Machines',
            text='Select a Virtual Machine from the menu'
        )

        menu.display()

    def network_menu(self):
        self.dialog.infobox(
            text='Retrieving information ...',
            width=40
        )

        view = self.agent.get_container_view(
            obj_type=[pyVmomi.vim.Network]
        )

        properties = self.agent.collect_properties(
            view_ref=view,
            obj_type=pyVmomi.vim.Network,
            path_set=['name', 'summary.accessible'],
            include_mors=True
        )
        view.DestroyView()

        items = [
            pvc.widget.menu.MenuItem(
                tag=network['name'],
                description='Accessible' if network['summary.accessible'] else 'Not Accessible',
                on_select=pvc.widget.network.NetworkWidget,
                on_select_args=(self.agent, self.dialog, network['obj'])
            ) for network in properties
        ]

        menu = pvc.widget.menu.Menu(
            items=items,
            dialog=self.dialog,
            title='Networks',
            text='Select a network from the menu that you wish to manage'
        )

        menu.display()


class InventorySearchWidget(object):
    def __init__(self, agent, dialog):
        """
        Inventory search widget

        Args:
            agent (VConnector): A VConnector instance
            dialog    (Dialog): A Dialog instance

        """
        self.agent = agent
        self.dialog = dialog
        self.display()

    def display(self):
        items = [
            pvc.widget.menu.MenuItem(
                tag='Hosts',
                description='Search inventory for hosts'
            ),
            pvc.widget.menu.MenuItem(
                tag='Virtual Machines',
                description='Search inventory for VMs'
            ),
        ]

        menu = pvc.widget.menu.Menu(
            items=items,
            dialog=self.dialog,
            title='Inventory Search',
            text=''
        )

        menu.display()
